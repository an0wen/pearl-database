#!/usr/bin/env python3
"""Convert Wicks et al. (2018) Supplementary Table S1 to PEARL SI tables."""

from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
RAW = HERE / "wicks2018_tableS1_thermo_raw.dat"

OUT = {
    7: HERE / "wicks2018_fe7si_thermo.dat",
    15: HERE / "wicks2018_fe15si_thermo.dat",
}

def parse_parenthetical(token):
    # Symmetric: 140(20), 10.288(52)
    m = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)\(([0-9]+(?:\.[0-9]+)?)\)", token)
    if m:
        value_text, unc_text = m.groups()
        value = float(value_text)
        if "." in unc_text:
            unc = float(unc_text)
        else:
            decimals = len(value_text.split(".")[1]) if "." in value_text else 0
            unc = int(unc_text) * 10.0 ** (-decimals)
        return value, unc, unc

    # Asymmetric: 377(-15,+65), 906(-1.5,+52)
    m = re.fullmatch(
        r"([0-9]+(?:\.[0-9]+)?)\(-([0-9]+(?:\.[0-9]+)?),\+([0-9]+(?:\.[0-9]+)?)\)",
        token,
    )
    if m:
        value, minus, plus = m.groups()
        return float(value), float(minus), float(plus)

    raise ValueError(f"Cannot parse parenthetical token: {token!r}")

rows = {7: [], 15: []}

for line in RAW.read_text().splitlines():
    if not line or line.startswith("#"):
        continue
    fields = line.split("\t")
    p_token = fields[0]
    wt_si = int(fields[3])
    rho_token = fields[11]

    P_GPa, dP_minus_GPa, dP_plus_GPa = parse_parenthetical(p_token)
    rho_gcm3, drho_gcm3, drho_plus = parse_parenthetical(rho_token)
    if abs(drho_gcm3 - drho_plus) > 0:
        raise ValueError("Density uncertainty unexpectedly asymmetric")

    rows[wt_si].append((
        rho_gcm3 * 1000.0,
        drho_gcm3 * 1000.0,
        P_GPa * 1e9,
        dP_minus_GPa * 1e9,
        dP_plus_GPa * 1e9,
    ))

for wt_si, path in OUT.items():
    lines = ["rho[kg/m^3]\tdrho[kg/m^3]\tP[Pa]\tdP_minus[Pa]\tdP_plus[Pa]"]
    for rho, drho, P, dPm, dPp in rows[wt_si]:
        lines.append(
            f"{rho:.12g}\t{drho:.12g}\t{P:.12g}\t{dPm:.12g}\t{dPp:.12g}"
        )
    path.write_text("\n".join(lines) + "\n")
