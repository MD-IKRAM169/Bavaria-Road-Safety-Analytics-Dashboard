#!/usr/bin/env python3
"""Summarize Power BI report layout from a PBIX (or a ZIP containing a PBIX).

Reads report layout metadata only. Does not extract, execute, or decode the data model.
This is not a Power BI renderer or a malware scanner.
"""
import argparse
import io
import json
from pathlib import Path
import sys
import zipfile

MAX_LAYOUT_BYTES = 16 * 1024 * 1024
MAX_PBIX_BYTES = 100 * 1024 * 1024


def _load_pbix(path):
    if path.suffix.lower() == '.pbix':
        return zipfile.ZipFile(path)
    with zipfile.ZipFile(path) as project:
        members = [item for item in project.infolist() if item.filename.lower().endswith('.pbix') and not item.is_dir()]
        if len(members) != 1:
            raise ValueError(f'Expected one .pbix file in project archive; found {len(members)}')
        if members[0].file_size > MAX_PBIX_BYTES:
            raise ValueError('PBIX exceeds the size limit for metadata inspection')
        return zipfile.ZipFile(io.BytesIO(project.read(members[0])))


def inspect(path):
    """Read visual definitions without loading the Power BI data model."""
    with _load_pbix(Path(path)) as report:
        info = report.getinfo('Report/Layout')
        if info.file_size > MAX_LAYOUT_BYTES:
            raise ValueError('Report layout exceeds the configured size limit')
        layout = json.loads(report.read(info).decode('utf-16-le'))
    pages = []
    for section in layout.get('sections', []):
        visuals = []
        for container in section.get('visualContainers', []):
            try:
                config = json.loads(container.get('config') or '{}')
            except (ValueError, TypeError):
                continue
            visual = config.get('singleVisual', {})
            visual_type = visual.get('visualType')
            if not visual_type:
                continue
            projections = {}
            for role, items in visual.get('projections', {}).items():
                projections[role] = [item.get('queryRef') for item in items if item.get('queryRef')]
            visuals.append({'type': visual_type, 'fields_by_role': projections})
        pages.append({'name': section.get('displayName') or section.get('name'),
                      'width': section.get('width'), 'height': section.get('height'),
                      'visuals': visuals, 'visual_count': len(visuals)})
    return {'page_count': len(pages), 'pages': pages,
            'caveat': 'Report metadata only: no data model values, DAX definitions or rendered screenshots were independently verified.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path, help='Power BI .pbix file or original project .zip')
    parser.add_argument('--output', type=Path, help='Write the metadata report as JSON')
    args = parser.parse_args(argv)
    try:
        result = inspect(args.file)
    except (OSError, KeyError, ValueError, UnicodeError, zipfile.BadZipFile) as exc:
        print(f'Cannot inspect PBIX layout: {exc}', file=sys.stderr)
        return 1
    print(f"Report pages: {result['page_count']}")
    for page in result['pages']:
        print(f"  {page['name']}: {page['visual_count']} visual types")
        for visual in page['visuals']:
            print(f"    {visual['type']}: {visual['fields_by_role']}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'Metadata saved to {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
