#!/usr/bin/env python3
"""Convert Ono & Oganov (2005) Table 4 MgSiO3 phase-stability points to SI."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "ono2005_mgsio3_phase_stability_raw.dat"
DST = HERE / "ono2005_mgsio3_phase_stability.dat"

PHASE = {
    "A": "bridgmanite",
    "B": "post-perovskite",
}

def main():
    rows = []
    with SRC.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("P["):
                continue
            p, dp, t, dt, result = line.rstrip("\n").split("\t")
            rows.append((
                float(p) * 1e9,
                float(dp) * 1e9,
                float(t),
                float(dt),
                PHASE[result],
            ))
    with DST.open("w", newline="") as f:
        f.write("P[Pa]\tdP[Pa]\tT[K]\tdT[K]\tphase\n")
        for p, dp, t, dt, phase in rows:
            f.write(f"{p:.12g}\t{dp:.12g}\t{t:.12g}\t{dt:.12g}\t{phase}\n")

if __name__ == "__main__":
    main()
