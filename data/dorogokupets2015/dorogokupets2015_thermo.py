#!/usr/bin/env python3
from pathlib import Path

HERE = Path(__file__).resolve().parent

V0_CM3 = {
    "forsterite": 43.67,
    "wadsleyite": 40.54,
    "ringwoodite": 39.5,
    "bridgmanite": 24.45,
    "akimotoite": 26.35,
    "postperovskite": 24.2,
}
M_KG_PER_MOL = {
    "forsterite": 0.1406931,
    "wadsleyite": 0.1406931,
    "ringwoodite": 0.1406931,
    "bridgmanite": 0.1003887,
    "akimotoite": 0.1003887,
    "postperovskite": 0.1003887,
}

def convert(label):
    src = HERE / f"dorogokupets2015_{label}_thermo_raw.dat"
    dst = HERE / f"dorogokupets2015_{label}_thermo.dat"
    out = []
    with src.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("P["):
                continue
            P,T,x,alpha,S,Cp,Cv,KT,KS,gamma,Kprime,G = line.rstrip("\n").split("\t")
            V = float(x) * V0_CM3[label] * 1e-6
            rho = M_KG_PER_MOL[label] / V
            out.append((
                rho, float(P)*1e9, float(T), V,
                float(S), float(Cp), float(Cv),
                float(alpha)*1e-6, float(KT)*1e9, float(KS)*1e9,
                float(gamma), float(Kprime), float(G)*1e3
            ))
    with dst.open("w", newline="") as f:
        f.write("rho[kg/m^3]\tP[Pa]\tT[K]\tV[m^3/mol]\ts[J/mol/K]\tcp[J/mol/K]\tcv[J/mol/K]\talpha[1/K]\tKT[Pa]\tKS[Pa]\tgamma\tKprime\tg[J/mol]\n")
        for r in out:
            f.write("\t".join(f"{v:.12g}" for v in r)+"\n")

def main():
    for label in V0_CM3:
        convert(label)

if __name__ == "__main__":
    main()
