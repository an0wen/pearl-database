#!/usr/bin/env python3
from pathlib import Path

N_A = 6.02214076e23          # mol^-1, exact SI definition
Z = 2                        # H2O formula units in the indexed cell
MOLAR_MASS = 18.01528e-3     # kg/mol

P_VII_TO_VIIT = 5.1e9        # Pa, final-paper nominal transition
P_VIIT_TO_X = 30.9e9         # Pa, final-paper nominal transition

HERE = Path(__file__).resolve().parent
RAW = HERE / "grande2022_table4_thermo_raw.dat"

OUTPUTS = {
    "icevii": HERE / "grande2022_icevii_thermo.dat",
    "iceviit": HERE / "grande2022_iceviit_thermo.dat",
    "icex": HERE / "grande2022_icex_thermo.dat",
}

def classify(P):
    if P <= P_VII_TO_VIIT:
        return "icevii"
    if P <= P_VIIT_TO_X:
        return "iceviit"
    return "icex"

rows = {key: [] for key in OUTPUTS}

for line in RAW.read_text().splitlines():
    if not line or line.startswith("#"):
        continue
    p_gpa, dp_gpa, vcell_a3 = line.split()
    P = float(p_gpa) * 1e9
    dP = float(dp_gpa) * 1e9
    Vcell = float(vcell_a3)
    V = Vcell * 1e-30 * N_A / Z
    rho = MOLAR_MASS / V
    rows[classify(P)].append((rho, P, dP, V))

for phase, path in OUTPUTS.items():
    lines = ["rho[kg/m^3]\tP[Pa]\tdP[Pa]\tV[m^3/mol]"]
    for rho, P, dP, V in rows[phase]:
        lines.append(f"{rho:.12g}\t{P:.12g}\t{dP:.12g}\t{V:.12g}")
    path.write_text("\n".join(lines) + "\n")
