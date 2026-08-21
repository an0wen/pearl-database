#!/usr/bin/env python3
"""Convert the Li et al. (2023) SiO2 TVPF supplementary data to PEARL draft TSV files.

Uses only the Python standard library. It reads the Office Open XML package
directly, preserves source row order, and converts reported units to SI.

Reported supplementary quantities: T [K], V [cm^3/mol], P [GPa], F [kJ/mol].
Derived quantity: rho = M_SiO2 / V using adopted M_SiO2 = 0.0600843 kg/mol
(NIST Chemistry WebBook molecular weight 60.0843 g/mol).
"""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_OFFICE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL_PACKAGE = "http://schemas.openxmlformats.org/package/2006/relationships"
M_SIO2 = Decimal("0.0600843")  # kg/mol; adopted, not reported by Li et al. (2023)

PHASE_LABELS = {
    "stishovite": "stishovite",
    "CaCl2-type SiO2": "cacl2sio2",
    "seifertite": "seifertite",
}


def column_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        raise ValueError(f"Invalid cell reference: {cell_ref!r}")
    value = 0
    for char in match.group(1):
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value - 1


def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    strings: list[str] = []
    for si in root.findall(f"{{{NS_MAIN}}}si"):
        text = "".join(node.text or "" for node in si.iter(f"{{{NS_MAIN}}}t"))
        strings.append(text)
    return strings


def worksheet_targets(archive: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    rel_targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall(f"{{{NS_REL_PACKAGE}}}Relationship")
    }
    targets: dict[str, str] = {}
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
    if sheets is None:
        raise ValueError("Workbook contains no sheets")
    for sheet in sheets.findall(f"{{{NS_MAIN}}}sheet"):
        name = sheet.attrib["name"]
        rid = sheet.attrib[f"{{{NS_REL_OFFICE}}}id"]
        target = rel_targets[rid]
        if not target.startswith("xl/"):
            target = "xl/" + target.lstrip("/")
        targets[name] = target
    return targets


def read_sheet(path: Path, sheet_name: str) -> list[list[str | None]]:
    with zipfile.ZipFile(path) as archive:
        strings = shared_strings(archive)
        targets = worksheet_targets(archive)
        if sheet_name not in targets:
            raise KeyError(f"Worksheet {sheet_name!r} not found; available: {sorted(targets)}")
        root = ET.fromstring(archive.read(targets[sheet_name]))
        sheet_data = root.find(f"{{{NS_MAIN}}}sheetData")
        if sheet_data is None:
            return []
        rows: list[list[str | None]] = []
        for row_node in sheet_data.findall(f"{{{NS_MAIN}}}row"):
            row_values: list[str | None] = []
            for cell in row_node.findall(f"{{{NS_MAIN}}}c"):
                ref = cell.attrib.get("r", "")
                idx = column_index(ref)
                while len(row_values) <= idx:
                    row_values.append(None)
                cell_type = cell.attrib.get("t")
                if cell_type == "inlineStr":
                    is_node = cell.find(f"{{{NS_MAIN}}}is")
                    value = "" if is_node is None else "".join(
                        node.text or "" for node in is_node.iter(f"{{{NS_MAIN}}}t")
                    )
                else:
                    value_node = cell.find(f"{{{NS_MAIN}}}v")
                    if value_node is None or value_node.text is None:
                        value = None
                    elif cell_type == "s":
                        value = strings[int(value_node.text)]
                    else:
                        value = value_node.text
                row_values[idx] = value
            rows.append(row_values)
        return rows


def as_decimal(value: str | None, field: str) -> Decimal:
    if value is None or value == "":
        raise ValueError(f"Missing numeric value for {field}")
    return Decimal(value)


def scientific(value: Decimal) -> str:
    if value.is_zero():
        return "0"
    normalized = value.normalize()
    exponent = normalized.adjusted()
    coefficient = normalized.scaleb(-exponent).normalize()
    return f"{coefficient}e{exponent:+d}"


def round_significant(value: Decimal, digits: int) -> Decimal:
    if value.is_zero():
        return value
    with localcontext() as ctx:
        ctx.prec = max(30, digits + 5)
        quantum = Decimal(1).scaleb(value.adjusted() - digits + 1)
        return value.quantize(quantum)


def significant(value: Decimal, digits: int) -> str:
    return scientific(round_significant(value, digits))


def plain(value: Decimal) -> str:
    return format(value.normalize(), "f")


def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.write_text(
        "\t".join(header) + "\n" + "\n".join("\t".join(row) for row in rows) + "\n",
        encoding="utf-8",
    )


def convert_tvpf(workbook: Path, output_dir: Path) -> dict[str, int]:
    rows = read_sheet(workbook, "TVPF")
    grouped: dict[str, list[list[str]]] = {key: [] for key in PHASE_LABELS.values()}
    for row in rows:
        phase = row[0] if row else None
        if phase not in PHASE_LABELS:
            continue
        if len(row) < 5:
            raise ValueError(f"Incomplete TVPF row for {phase}: {row}")
        temperature = as_decimal(row[1], "T").quantize(Decimal("1"))
        volume_cm3 = as_decimal(row[2], "V").quantize(Decimal("0.0001"))
        pressure_gpa = round_significant(as_decimal(row[3], "P"), 15)
        free_kj = round_significant(as_decimal(row[4], "F"), 15)
        volume_si = volume_cm3 * Decimal("1e-6")
        pressure_si = pressure_gpa * Decimal("1e9")
        free_si = free_kj * Decimal("1e3")
        density_si = M_SIO2 / volume_si
        grouped[PHASE_LABELS[phase]].append([
            significant(density_si, 6),
            scientific(pressure_si),
            plain(temperature),
            scientific(volume_si),
            scientific(free_si),
        ])
    for label, data in grouped.items():
        write_tsv(
            output_dir / f"li2023_{label}_thermo.dat",
            ["rho[kg/m^3]", "P[Pa]", "T[K]", "V[m^3/mol]", "f[J/mol]"],
            data,
        )
    return {label: len(data) for label, data in grouped.items()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).with_name("li2023_sio2_thermo_raw.xlsx"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    tvpf_counts = convert_tvpf(args.input, args.output_dir)
    print("TVPF rows:", tvpf_counts)


if __name__ == "__main__":
    main()
