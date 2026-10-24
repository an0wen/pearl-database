"""Generate contributor templates: python scripts/generate_templates.py."""
import argparse
from pathlib import Path
from schema_utils import ROOT, load_schemas, sections, toml_value


def generate(output_dir=ROOT / 'data' / '_template'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for kind, schema in load_schemas().items():
        lines = [f'# Generated from schemas/{kind}.toml; do not edit directly.',
                 '# Values are examples, not automatic defaults.', '# ' + schema['description'], '']
        for section, fields in sections(schema).items():
            fields = {name: field for name, field in fields.items() if field.get('template', True)}
            note = schema.get('sections', {}).get(section, {}).get('description')
            if not fields and not note:
                continue
            if section:
                lines.append(f'[{section}]')
            if note:
                lines.append('# ' + note)
            for name, field in fields.items():
                required = 'yes' if field['required'] else 'no'
                lines.append(f'{name} = {toml_value(field["example"])}  # {field["description"]} | Unit: {field["unit"]} | Required: {required}')
            lines.append('')
        target = output_dir / schema['template_file']
        target.write_text('\n'.join(lines), encoding='utf-8')
        print(f'Generated {target}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'data' / '_template')
    generate(parser.parse_args().output_dir)
