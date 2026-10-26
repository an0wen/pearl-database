"""Shared schema loading and rendering helpers (Python 3.11+; standard library only)."""
from collections import OrderedDict
import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / 'schemas'
KINDS = ('source', 'eos', 'thermo')


def load_schemas(directory=SCHEMA_DIR):
    """Resolve cross-schema references, rejecting missing targets and cycles."""
    raw = {}
    for kind in KINDS:
        with (Path(directory) / f'{kind}.toml').open('rb') as stream:
            raw[kind] = tomllib.load(stream)

    def resolve(kind, name, trail=()):
        identity = (kind, name)
        if identity in trail:
            raise ValueError(f'Cyclic schema reference: {trail + (identity,)}')
        try:
            definition = raw[kind]['fields'][name].copy()
        except KeyError as error:
            raise ValueError(f'Unknown schema reference: {kind}:{name}') from error
        reference = definition.pop('ref', None)
        if reference:
            target_kind, target_name = reference.split(':', 1)
            definition = {**resolve(target_kind, target_name, trail + (identity,)), **definition}
        for attribute in ('type', 'description', 'unit', 'required', 'example'):
            if attribute not in definition:
                raise ValueError(f'{kind}:{name} lacks {attribute}')
        return definition

    return {kind: {**schema, 'fields': {
        name: resolve(kind, name) for name in schema['fields']
    }} for kind, schema in raw.items()}


def sections(schema):
    """Group dotted field paths while preserving schema order."""
    result = OrderedDict()
    for path, definition in schema['fields'].items():
        section, _, name = path.rpartition('.')
        result.setdefault(section, OrderedDict())[name] = definition
    for section in schema.get('sections', {}):
        result.setdefault(section, OrderedDict())
    return result


def toml_value(value):
    # JSON strings, booleans, numbers and homogeneous arrays are valid TOML values.
    return json.dumps(value, ensure_ascii=False, allow_nan=False)


def field_paths(value, prefix=''):
    """Yield exact leaf paths, including keys within arrays of tables."""
    for key, content in value.items():
        path = f'{prefix}.{key}' if prefix else key
        if isinstance(content, dict):
            if content:
                yield from field_paths(content, path)
            else:
                yield path
        elif isinstance(content, list) and content and all(isinstance(v, dict) for v in content):
            for item in content:
                yield from field_paths(item, path)
        else:
            yield path
