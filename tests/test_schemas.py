"""Test schema tools using temporary fixtures, without scanning repository data.

Run with python tests/test_schemas.py (optionally --verbose).
"""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from schema_utils import load_schemas
from generate_templates import generate
from generate_schema_docs import generate as generate_docs
from check_schema_coverage import check


class SchemaTests(unittest.TestCase):
    def test_kind_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for kind in ('source', 'eos', 'thermo'):
                (root / f'example_{kind}.toml').write_text('unknown = 1\n')
            for selected in ('all', 'source', 'eos', 'thermo'):
                with self.subTest(kind=selected):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        self.assertEqual(check(root, kind=selected), 1)
                    for kind in ('source', 'eos', 'thermo'):
                        self.assertEqual(f'UNDEFINED {kind}: unknown' in output.getvalue(),
                                         selected == 'all' or selected == kind)
            (root / 'example_thermo.toml').write_text('broken = [')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(check(root, kind='source'), 1)
                self.assertEqual(check(root), 2)

    def test_references_and_generated_outputs(self):
        schemas = load_schemas()
        for kind in ('eos', 'thermo'):
            self.assertEqual(schemas['source']['fields']['unique_id'],
                             schemas[kind]['fields']['unique_id'])
        self.assertEqual(schemas['eos']['fields']['science.material'],
                         schemas['thermo']['fields']['science.material'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with contextlib.redirect_stdout(io.StringIO()):
                generate(root)
            for kind, schema in schemas.items():
                path = root / schema['template_file']
                data = tomllib.loads(path.read_text())
                self.assertEqual(data['unique_id'], 'template2026')
                for line in path.read_text().splitlines():
                    if line and not line.startswith(('#', '[')):
                        self.assertIn(' | Unit: ', line)
                        self.assertIn(' | Required: ', line)
            generate_docs(root / 'reference.rst')
            doc = (root / 'reference.rst').read_text()
            self.assertEqual(doc.count('Data file reference'), 1)
            self.assertIn('science\n~~~~~~~', doc)
            self.assertNotIn('``science.material``', doc)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(check(root), 0)

    def test_bad_references_fail_explicitly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for kind in ('source', 'eos', 'thermo'):
                (root / f'{kind}.toml').write_text('[fields.x]\nref = "source:x"\n')
            with self.assertRaisesRegex(ValueError, 'Cyclic'):
                load_schemas(root)
            (root / 'source.toml').write_text('[fields.x]\nref = "source:missing"\n')
            with self.assertRaisesRegex(ValueError, 'Unknown schema reference'):
                load_schemas(root)

    def test_source_links_are_reported(self):
        # Keep the regression independent of additions to the real source schema.
        schemas = load_schemas()
        schemas['source']['fields'] = {}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'example_source.toml').write_text(
                'ads = "https://ui.adsabs.harvard.edu/example"\n'
                'zenodo = "https://zenodo.org/records/123"\n')
            (root / 'nested_source.toml').write_text(
                '[github]\nlink = "https://github.com/example/repo"\n'
                '[zenodo]\ndoi = "https://doi.org/10.5281/zenodo.123"\n'
                'link = "https://zenodo.org/records/123"\n')
            output = io.StringIO()
            with contextlib.redirect_stdout(output), patch('check_schema_coverage.load_schemas', return_value=schemas):
                self.assertEqual(check(root), 1)
            for field in ('ads', 'zenodo', 'github.link', 'zenodo.doi', 'zenodo.link'):
                self.assertIn(f'UNDEFINED source: {field}\n', output.getvalue())

    def test_nested_unknown_and_invalid_toml(self):
        for kind in ('source', 'eos', 'thermo'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                self.check_unknown_and_invalid_toml(Path(directory), kind)

    def check_unknown_and_invalid_toml(self, root, kind):
        path = root / f'_draft_{kind}.toml'
        path.write_text('[custom.nested]\nunknown = 1\n')
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(check(root), 1)
        self.assertIn('custom.nested.unknown', output.getvalue())
        self.assertIn(f'UNDEFINED {kind}: custom.nested.unknown', output.getvalue())
        self.assertIn(f'_draft_{kind}.toml', output.getvalue())
        path.write_text('broken = [')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(check(root), 2)


if __name__ == '__main__':
    unittest.main()
