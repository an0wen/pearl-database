#!/usr/bin/env python3
"""Reproduce Wolf & Bower (2018) S11 per-atom -> SI molar conversions.

This script does not reproduce the RTpress fit. It only documents deterministic
unit/basis conversions used in the PEARL EOS metadata and compares them with
the rounded MAGRATHEA implementation constants.
"""
NA = 6.02214076e23
EV_J = 1.602176634e-19
N_ATOMS = 5

V0_A3_ATOM = 12.949
B_EV_ATOM = [0.9821, 0.615, 1.31, -3.0, -4.1]

v0_m3_mol = V0_A3_ATOM * 1e-30 * N_ATOMS * NA
b_j_mol = [b * EV_J * N_ATOMS * NA for b in B_EV_ATOM]

print("V0 [m^3/mol] =", repr(v0_m3_mol))
print("V0 [cm^3/mol] =", repr(v0_m3_mol * 1e6))
print("b_n [J/mol] =", b_j_mol)
print("b_n [erg/mol] =", [x * 1e7 for x in b_j_mol])

# MAGRATHEA EOSlist.cpp rounded implementation:
mag_v0_cm3_mol = 38.99
mag_b_erg_mol = [4.738e12, 2.97e12, 6.32e12, -1.4e13, -2.0e13]
print("MAGRATHEA V0 [cm^3/mol] =", mag_v0_cm3_mol)
print("MAGRATHEA b_n [erg/mol] =", mag_b_erg_mol)
