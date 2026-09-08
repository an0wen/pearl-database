#!/usr/bin/env python3
"""Convert Smith et al. (2018) Supplementary Table 1a to PEARL SI format."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "smith2018_fe-isentrope_thermo_raw.dat"
DST = HERE / "smith2018_fe-isentrope_thermo.dat"

def main():
    rows = []
    with SRC.open() as f:
        for line in f:
            if line.startswith("#") or line.startswith("P[") or not line.strip():
                continue
            p_gpa, dp_gpa, rho_gcc, drho_gcc = line.rstrip("\n").split("\t")
            rows.append((
                float(rho_gcc) * 1000.0,
                float(drho_gcc) * 1000.0,
                float(p_gpa) * 1.0e9,
                float(dp_gpa) * 1.0e9,
            ))
    with DST.open("w", newline="") as f:
        f.write("rho[kg/m^3]\tdrho[kg/m^3]\tP[Pa]\tdP[Pa]\n")
        for rho, drho, p, dp in rows:
            f.write(f"{rho:.12g}\t{drho:.12g}\t{p:.12g}\t{dp:.12g}\n")

if __name__ == "__main__":
    main()
