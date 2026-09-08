#!/usr/bin/env python3
from pathlib import Path
import csv

HERE = Path(__file__).resolve().parent
NA = 6.02214076e23
EV_J = 1.602176634e-19

def conv_v(v_a3_atom):
    return v_a3_atom * 1e-30 * NA  # m^3/mol C

def conv_e(e_ev_atom):
    return e_ev_atom * EV_J * NA   # J/mol C

def convert4(src, dst):
    with src.open() as f:
        rr = list(csv.DictReader(f, delimiter="\t"))
    with dst.open("w") as f:
        f.write("P[Pa]\tT[K]\tV[m^3/mol]\tu[J/mol]\n")
        for r in rr:
            p = float(r["P[GPa]"])*1e9
            t = float(r["T[K]"])
            v = conv_v(float(r["V[Angstrom^3/atom]"]))
            u = conv_e(float(r["E[eV/atom]"]))
            f.write(f"{p:.15g}\t{t:.15g}\t{v:.15g}\t{u:.15g}\n")

def convert6(src, dst):
    with src.open() as f:
        rr = list(csv.DictReader(f, delimiter="\t"))
    with dst.open("w") as f:
        f.write("P[Pa]\tdP[Pa]\tT[K]\tV[m^3/mol]\tu[J/mol]\tdu[J/mol]\n")
        for r in rr:
            p = float(r["P[GPa]"])*1e9
            dp = float(r["dP[GPa]"])*1e9
            t = float(r["T[K]"])
            v = conv_v(float(r["V[Angstrom^3/atom]"]))
            u = conv_e(float(r["E[eV/atom]"]))
            du = conv_e(float(r["dE[eV/atom]"]))
            f.write(f"{p:.15g}\t{dp:.15g}\t{t:.15g}\t{v:.15g}\t{u:.15g}\t{du:.15g}\n")

convert4(HERE/"benedict2014_diamond-dftmd_thermo_raw.dat",
         HERE/"benedict2014_diamond-dftmd_thermo.dat")
convert4(HERE/"benedict2014_liquid-dftmd_thermo_raw.dat",
         HERE/"benedict2014_liquid-dftmd_thermo.dat")
convert6(HERE/"benedict2014_liquid-pimc_thermo_raw.dat",
         HERE/"benedict2014_liquid-pimc_thermo.dat")
