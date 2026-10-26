# Shared data schemas

Edit `source.toml`, `eos.toml`, and `thermo.toml` here. Field paths use dotted
section names; root fields have no dot. References such as
`ref = "eos:science.material"` reuse another field, with local attributes taking
precedence. Missing references and reference cycles are errors.

Each resolved field specifies `type`, `description`, `unit`, `required`, and
`example`. `allow_list = true` describes either a scalar or a list of the stated
type. `format` adds a format description, such as `doi-url`. These attributes
are metadata for the templates and documentation; value validation is not
implemented by the coverage checker. Required means present, independently of
whether a value is empty. Examples are not defaults. `template = false` keeps a
field in the reference but omits it from the contributor template.

Run from the repository root with Python 3.11 or later (no added dependencies):

```sh
python scripts/generate_templates.py
python scripts/generate_schema_docs.py
python scripts/check_schema_coverage.py
```

The first command overwrites the three generated files in `data/_template`.
Every assignment includes its description, unit and required status on one line.
The second writes a single Sphinx page with a table per section, grouped by
source, EOS and thermo. The Sphinx build also regenerates that page automatically.
Commit schema changes together with regenerated templates and documentation.

The checker scans all `*_source.toml`, `*_eos.toml`, and `*_thermo.toml` files
recursively, including templates and underscore-prefixed entries. It prints
undefined fields grouped by schema and field, followed by the affected paths.
It skips other file kinds, including phase-boundary TOML files and table contents.
Use `--data-dir PATH` to inspect another directory. Exit codes are 0 for complete
coverage, 1 for undefined fields, and 2 for read or TOML parse errors.

The initial schemas describe the contributor template fields and a few common
metadata fields. Existing model-specific parameters and extended provenance
will be reported until their definitions are reviewed and added. No wildcard
sections silently suppress these reports. The empty EOS `parameters` section
has guidance but does not declare arbitrary parameter names as known fields.

Run `python tests/test_schemas.py` to test the schema tools using temporary
fixtures. It does not scan repository data. Add `--verbose` for detailed unittest
results, or use `python -m unittest discover -s tests -p test_schemas.py`.

Run `python scripts/check_schema_coverage.py` to check actual repository data.
Select one metadata kind with `--kind source`, `--kind eos`, or `--kind thermo`.
Omitting the option (or passing `--kind all`) checks all three.
