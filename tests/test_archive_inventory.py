"""Standard-library tests of safe metadata inspection."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('archive_inventory', ROOT / 'tools' / 'archive_inventory.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ArchiveInventoryTests(unittest.TestCase):
    def test_inventory_and_extensions(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'example.zip'
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('reports/project.pbix', 'dummy')
                z.writestr('data/sample.csv', 'value\n1\n')
            result = mod.inventory(path, include_hash=True)
            self.assertEqual(result['member_count'], 2)
            self.assertEqual(result['extension_counts']['.pbix'], 1)
            self.assertEqual(result['extension_counts']['.csv'], 1)
            self.assertEqual(len(result['sha256']), 64)
            self.assertFalse(result['warnings'])

    def test_unsafe_paths_are_flagged_not_extracted(self):
        for name in ('../secrets.txt', '/tmp/secrets.txt', 'C:/secrets.txt', '..\\secret.txt'):
            self.assertTrue(mod.unsafe_member(name), name)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'danger.zip'
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('../secret.csv', 'private')
            result = mod.inventory(path)
            self.assertTrue(any('Unsafe archive path' in x for x in result['warnings']))
            self.assertFalse((Path(d).parent / 'secret.csv').exists())

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            mod.inventory(Path('this-archive-does-not-exist.zip'))


if __name__ == '__main__':
    unittest.main()
