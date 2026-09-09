#!/usr/bin/env python3
from pathlib import Path
import csv

NA = 6.02214076e23
M_SIC = 40.096e-3
Z = 4
HERE = Path(__file__).resolve().parent

def conv(Pgpa,dPgpa,T,Vcell,dVcell,dT=None):
    Vmol = Vcell*1e-30*NA/Z
    dVmol = dVcell*1e-30*NA/Z
    rho = M_SIC/Vmol
    drho = rho*dVcell/Vcell
    out=[rho,drho,Pgpa*1e9,dPgpa*1e9,T]
    if dT is not None:
        out.append(dT)
    return out+[Vmol,dVmol]

def write(path, header, rows):
    with path.open("w") as f:
        f.write("\t".join(header)+"\n")
        for row in rows:
            f.write("\t".join(f"{x:.15g}" for x in row)+"\n")

with (HERE/"miozzi2018_b3sic_thermo_raw.dat").open() as f:
    rr=list(csv.DictReader(f,delimiter="\t"))
b3=[conv(float(r["P_GPa"]),float(r["dP_GPa"]),float(r["T_measured_K"]),
         float(r["V_SiC_B3_A3"]),float(r["error_V_SiC_B3_A3"])) for r in rr]
write(HERE/"miozzi2018_b3sic_thermo.dat",
      ["rho[kg/m^3]","drho[kg/m^3]","P[Pa]","dP[Pa]","T[K]","V[m^3/mol]","dV[m^3/mol]"],b3)

with (HERE/"miozzi2018_b1sic_thermo_raw.dat").open() as f:
    rr=list(csv.DictReader(f,delimiter="\t"))
b1=[conv(float(r["P_GPa"]),float(r["dP_GPa"]),float(r["T_K"]),
         float(r["V_SiC_B1_A3"]),float(r["dV_SiC_B1_A3"]),float(r["dT_K"])) for r in rr]
write(HERE/"miozzi2018_b1sic_thermo.dat",
      ["rho[kg/m^3]","drho[kg/m^3]","P[Pa]","dP[Pa]","T[K]","dT[K]","V[m^3/mol]","dV[m^3/mol]"],b1)
