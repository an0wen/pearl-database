#!/usr/bin/env python3
"""Convert Journaux et al. (2020) Table 4 PVT data to phase-specific SI files."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "journaux2020_ice-pvt_thermo_raw.dat"

def main():
    groups = {}
    with SRC.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("phase\t"):
                continue
            phase, p_mpa, t_k, v_a3 = line.rstrip("\n").split("\t")
            groups.setdefault(phase, []).append((float(p_mpa), float(t_k), float(v_a3)))
    for phase, rows in groups.items():
        dst = HERE / f"journaux2020_{phase}_thermo.dat"
        with dst.open("w", newline="") as f:
            f.write("P[Pa]\tdP[Pa]\tT[K]\tdT[K]\tV_cell[m^3]\tdV_cell[m^3]\n")
            for p, t, v in rows:
                f.write(
                    f"{p*1e6:.12g}\t{30e6:.12g}\t{t:.12g}\t{0.5:.12g}\t"
                    f"{v*1e-30:.12g}\t{5e-33:.12g}\n"
                )

if __name__ == "__main__":
    main()
