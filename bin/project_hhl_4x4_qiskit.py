#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-06-07

import argparse
import math
import numpy as np
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2 as FakeProvider
from qiskit.circuit.library import QFT, RYGate, UnitaryGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='PHYS440 Project: HHL on 4x4 system.')
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--verbose", action="store_true", help="Verbose output")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
args = parser.parse_args()

# Set up matrices and vectors
A = np.array([[5/6, -1/3, 0, -1/6], [-1/3, 5/6, -1/6, 0], [0, -1/6, 5/6, -1/3], [-1/6, 0, -1/3, 5/6]])
b = np.array([1, 15, 3, 2])
λ, V = np.linalg.eig(A)

if args.verbose:
    Λ = np.diag(λ)
    Aprime = V @ Λ @ np.linalg.inv(V)
    print("Original matrix:\n", A)
    print("\nEigenvalues:\n", λ)
    print("\nEigenvectors:\n", V)
    print("\nDiagonal matrix of eigenvalues:\n", Λ)
    print("\nReconstructed matrix:\n", Aprime)

t = 3 * math.pi / 4
exp_A = np.diag(np.exp(1j * t * λ))
U1 = V @ exp_A @ np.linalg.inv(V)
U2 = U1 @ U1
U4 = U2 @ U2
invU1 = np.linalg.inv(U1)
invU2 = invU1 @ invU1
invU4 = invU2 @ invU2

if args.verbose:
    print("\nexp(iAt):\n", exp_A)
    print("\nU:\n", U1)
    print("\nU^2:\n", U2)
    print("\nU^4:\n", U4)
    print("\nU^(-1):\n", invU1)
    print("\nU^(-2):\n", invU2)
    print("\nU^(-4):\n", invU4)

# Set up circuit

qa = QuantumRegister(1, 'a')
qc = QuantumRegister(3, 'c')
qb = QuantumRegister(2, 'b')
clbits = ClassicalRegister(6)
circuit = QuantumCircuit(qa, qc, qb, clbits)
circuit.initialize(b/np.linalg.norm(b), qb)
circuit.h(qc)
U1gate = UnitaryGate(U1, label=r"$U$").control(1)
U2gate = UnitaryGate(U2, label=r"$U^2$").control(1)
U4gate = UnitaryGate(U4, label=r"$U^4$").control(1)
circuit.append(U1gate, [qc[0], qb[1], qb[0]])
circuit.append(U2gate, [qc[1], qb[1], qb[0]])
circuit.append(U4gate, [qc[2], qb[1], qb[0]])
circuit.append(QFT(3).inverse(), qc)
theta1 = 2 * np.arcsin(1/4)
theta2 = 2 * np.arcsin(1/3)
theta3 = 2 * np.arcsin(1/2)
theta4 = 2 * np.arcsin(1/1)
r1 = RYGate(theta1).control(3, ctrl_state='100')
r2 = RYGate(theta2).control(3, ctrl_state='011')
r3 = RYGate(theta3).control(3, ctrl_state='010')
r4 = RYGate(theta4).control(3, ctrl_state='001')
circuit.append(r1, [qc[0], qc[1], qc[2], qa[0]])
circuit.append(r2, [qc[0], qc[1], qc[2], qa[0]])
circuit.append(r3, [qc[0], qc[1], qc[2], qa[0]])
circuit.append(r4, [qc[0], qc[1], qc[2], qa[0]])
circuit.append(QFT(3), qc)
invU4gate = UnitaryGate(invU4, label=r"$U^{-4}$").control(1)
invU2gate = UnitaryGate(invU2, label=r"$U^{-2}$").control(1)
invU1gate = UnitaryGate(invU1, label=r"$U^{-1}$").control(1)
circuit.append(invU4gate, [qc[2], qb[1], qb[0]])
circuit.append(invU2gate, [qc[1], qb[1], qb[0]])
circuit.append(invU1gate, [qc[0], qb[1], qb[0]])
circuit.barrier()
circuit.h(qc)
circuit.barrier()
circuit.measure([qa[0], qc[0], qc[1], qc[2], qb[0], qb[1]], clbits)

# Output and run:
if args.filename:
    circuit.draw(output="mpl", filename=args.filename)

if args.provider == 'aer':
    backend = AerSimulator()
else:
    backend = next(iter([backend for backend in FakeProvider().backends() if backend.name == args.provider]), None)

sampler = Sampler(backend)

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(circuit)

if args.isa_filename:
    isa_circuit.draw(output="mpl", filename=args.isa_filename)

job = sampler.run([isa_circuit], shots=args.shots)
result = job.result()
counts = result[0].data.c0.get_counts()
total = sum(counts.values())
a1_total = sum(val for bits, val in counts.items() if bits.endswith("1"))

# Print the results
for bits, val in sorted(counts.items()):
    if bits.endswith("1"):
        print(f"{bits}: {val/a1_total:.2f}")

print(f"Prob(ancilla |0⟩) = {a1_total/total:.2f}")
