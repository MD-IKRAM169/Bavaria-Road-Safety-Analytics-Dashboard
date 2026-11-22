#!/usr/bin/env python3
"""Inspect a ZIP project archive without extracting or executing any contents.

Example:
    python tools/archive_inventory.py "ROAD ACCIDENT.zip" --output archive-inventory.json

This is a metadata inventory, not a security scan and not a data analysis.
"""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


PROJECT_EXTENSIONS = {
    '.pbix': 'Power BI report', '.pbit': 'Power BI template',
    '.twb': 'Tableau workbook', '.twbx': 'Tableau packaged workbook',
    '.hyper': 'Tableau extract', '.ipynb': 'Jupyter notebook',
    '.py': 'Python source', '.r': 'R source', '.rmd': 'R Markdown',
    '.qmd': 'Quarto document', '.sql': 'SQL script',
    '.xlsx': 'Excel workbook', '.xls': 'Excel workbook',
    '.csv': 'CSV data', '.parquet': 'Parquet data',
    '.pdf': 'PDF document', '.pptx': 'PowerPoint presentation',
    '.html': 'HTML', '.png': 'PNG image', '.jpg': 'JPEG image',
    '.jpeg': 'JPEG image', '.json': 'JSON data',
}


def unsafe_member(name: str) -> bool:
    """Flag absolute/traversal/Windows drive paths, rather than extract them."""
    path = PurePosixPath(name.replace('\\', '/'))
    pieces = path.parts
    if name.startswith(('/', '\\')) or '..' in pieces:
        return True
    if pieces and (':' in pieces[0] or pieces[0].startswith('~')):
        return True
    return '\x00' in name


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def inventory(path: Path, include_hash=False) -> dict:
    """Return metadata only; never read/extract archived member bytes."""
    if not path.is_file():
        raise FileNotFoundError(path)
    counts = collections.Counter()
    sizes = collections.Counter()
    entries = []
    warnings = []
    with zipfile.ZipFile(path) as archive:
        for item in archive.infolist():
            name = item.filename
            ext = PurePosixPath(name).suffix.lower()
            if not item.is_dir():
                counts[ext or '[no extension]'] += 1
                sizes[ext or '[no extension]'] += item.file_size
            if unsafe_member(name):
                warnings.append(f'Unsafe archive path: {name}')
            kind = (item.external_attr >> 16) & 0xffff
            if stat.S_ISLNK(kind):
                warnings.append(f'Archive member is a symbolic link: {name}')
            if item.compress_size and item.file_size > max(100 * 1024 * 1024, item.compress_size * 1000):
                warnings.append(f'Unusually high compression ratio: {name}')
            entries.append({
                'path': name,
                'directory': item.is_dir(),
                'size_bytes': item.file_size,
                'compressed_bytes': item.compress_size,
                'type_hint': PROJECT_EXTENSIONS.get(ext, ''),
                'encrypted': bool(item.flag_bits & 1),
            })
        duplicate_names = [name for name, n in collections.Counter(i.filename for i in archive.infolist()).items() if n > 1]
        for name in duplicate_names:
            warnings.append(f'Duplicate archive member: {name}')
    result = {
        'archive_name': path.name,
        'archive_size_bytes': path.stat().st_size,
        'member_count': len(entries),
        'extension_counts': dict(sorted(counts.items())),
        'uncompressed_bytes_by_extension': dict(sorted(sizes.items())),
        'entries': entries,
        'warnings': warnings,
        'note': 'File extensions are hints only; no contents were executed or validated.',
    }
    if include_hash:
        result['sha256'] = sha256_file(path)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path, help='Path to the ZIP archive')
    parser.add_argument('--output', type=Path, help='Optional JSON output file')
    parser.add_argument('--sha256', action='store_true', help='Compute SHA-256 of the archive')
    args = parser.parse_args(argv)
    try:
        data = inventory(args.archive, include_hash=args.sha256)
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        print(f'Cannot inspect archive: {exc}', file=sys.stderr)
        return 1
    serialized = json.dumps(data, indent=2, ensure_ascii=False)
    print(f'Archive: {data["archive_name"]} ({data["archive_size_bytes"]:,} bytes)')
    print(f'Members: {data["member_count"]}')
    for ext, count in data['extension_counts'].items():
        print(f'  {ext}: {count}')
    for warning in data['warnings']:
        print(f'WARNING: {warning}')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + '\n', encoding='utf-8')
        print(f'Wrote inventory: {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
