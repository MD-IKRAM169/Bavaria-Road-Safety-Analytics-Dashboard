import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
import zipfile
import json

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('inspect_pbix', ROOT / 'tools' / 'inspect_pbix.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fake_pbix():
    layout = {'sections': [{'displayName': 'Demo', 'width': 1280, 'height': 720,
              'visualContainers': [{'config': json.dumps({'singleVisual': {'visualType': 'barChart',
              'projections': {'Y': [{'queryRef': 'Data.Casualties'}]}}})}]}]}
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, 'w') as z:
        z.writestr('Report/Layout', json.dumps(layout).encode('utf-16-le'))
    return bio.getvalue()


class InspectPBIXTests(unittest.TestCase):
    def test_direct_pbix(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'report.pbix'
            path.write_bytes(fake_pbix())
            report = module.inspect(path)
            self.assertEqual(report['page_count'], 1)
            self.assertEqual(report['pages'][0]['visuals'][0]['fields_by_role']['Y'], ['Data.Casualties'])

    def test_project_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'project.zip'
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('project/report.pbix', fake_pbix())
            self.assertEqual(module.inspect(path)['pages'][0]['visual_count'], 1)

    def test_zip_with_no_pbix(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'empty.zip'
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('x.txt', 'hello')
            with self.assertRaises(ValueError):
                module.inspect(path)


if __name__ == '__main__':
    unittest.main()
