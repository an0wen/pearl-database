"""Report fields present in data TOML files but absent from their schemas.

This checks schema coverage, not missing required values or scientific validity.
Exit status: 0 covered, 1 uncovered fields, 2 unreadable/invalid TOML.
"""
import argparse
from collections import defaultdict
from pathlib import Path
import tomllib
from schema_utils import ROOT, KINDS, field_paths, load_schemas


def check(data_dir, kind='all'):
    if kind not in (*KINDS, 'all'):
        raise ValueError(f'Unknown schema kind: {kind}')
    selected = KINDS if kind == 'all' else (kind,)
    schemas = load_schemas()
    missing = defaultdict(list)
    scanned = 0
    skipped = 0
    errors = 0
    for path in sorted(Path(data_dir).rglob('*.toml')):
        kind = next((k for k in KINDS if path.name.endswith(f'_{k}.toml')), None)
        if kind not in selected:
            skipped += 1
            continue
        scanned += 1
        try:
            with path.open('rb') as stream:
                data = tomllib.load(stream)
        except (OSError, tomllib.TOMLDecodeError) as error:
            print(f'ERROR {path}: {error}')
            errors += 1
            continue
        known = schemas[kind]['fields']
        # A declared child implies its parent table is known, even if empty.
        for field in sorted(set(field_paths(data))):
            if (field not in known
                    and field not in schemas[kind].get('sections', {})
                    and not any(k.startswith(field + '.') for k in known)):
                missing[kind, field].append(path)
    for (kind, field), paths in sorted(missing.items()):
        print(f'UNDEFINED {kind}: {field}')
        for path in paths:
            print(f'  {path}')
    print(f'Checked {scanned} {"/".join(selected)} TOML files (including templates and underscore-prefixed entries).')
    print(f'Skipped {skipped} TOML files outside the selection; .dat and raw files are outside metadata schema scope.')
    print(f'{len(missing)} undefined fields; {errors} parse/read errors.')
    return 2 if errors else int(bool(missing))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=ROOT / 'data')
    parser.add_argument('--kind', choices=('all', *KINDS), default='all',
                        help='Metadata kind to check (default: all).')
    args = parser.parse_args()
    if not args.data_dir.is_dir():
        parser.error(f'Data directory does not exist: {args.data_dir}')
    raise SystemExit(check(args.data_dir, kind=args.kind))
