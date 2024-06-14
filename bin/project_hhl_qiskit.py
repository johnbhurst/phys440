#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-06-10

import argparse
import csv
import math
import numpy as np
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2 as FakeProvider
from qiskit.circuit.library import QFT, RYGate, UnitaryGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='PHYS440 Project: HHL on arbitrary system.')
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--clockqubits", type=int, default=3, help="Number of clock qubits")
parser.add_argument("--decimals", type=int, default=4, help="Number of decimal places")
parser.add_argument("--scalingmode", type=str, default="half", help="Eigenvalue scaling mode (half, full) (default half)")
parser.add_argument("--verbose", action="store_true", help="Verbose output")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
parser.add_argument("a_filename", type=str, help="Filename for A matrix")
parser.add_argument("b_filename", type=str, help="Filename for b vector")
args = parser.parse_args()

# Set up matrices and vectors
def safe_eval(expr):
    allowed_names = {"pi": math.pi}
    return eval(expr, {"__builtins__": None}, allowed_names)

def read_matrix(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        matrix = [[safe_eval(entry) for entry in row] for row in reader]
    return np.array(matrix)

def read_vector(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        vector = [safe_eval(entry) for row in reader for entry in row]
    return np.array(vector)

A = read_matrix(args.a_filename)
b = read_vector(args.b_filename)
n = args.clockqubits
m = int(math.log2(len(b)))

if args.verbose:
    print(f"{A=}")
    print(f"{b=}")

λ, V = np.linalg.eig(A)

if args.verbose:
    Λ = np.diag(λ)
    Aprime = V @ Λ @ np.linalg.inv(V)
    print("Original matrix:\n", A)
    print("\nEigenvalues:\n", λ)
    print("\nEigenvectors:\n", V)
    print("\nDiagonal matrix of eigenvalues:\n", Λ)
    print("\nReconstructed matrix:\n", Aprime)

t = math.pi / max(λ)
exp_A = np.diag(np.exp(1j * t * λ))
U = V @ exp_A @ np.linalg.inv(V)
invU = np.linalg.inv(U)
U_matrices = [np.linalg.matrix_power(U, 2**i) for i in range(n)]
invU_matrices = [np.linalg.matrix_power(invU, 2**i) for i in range(n)]

if args.verbose:
    print("\t: ", t)
    print("\nexp(iAt):\n", exp_A)
    for i, U in enumerate(U_matrices):
        print(f"\nU^{2**i}:\n", U)
    for i, invU in enumerate(reversed(invU_matrices)):
        print(f"\nU^(-2^{n-i-1}):\n", invU)

# Set up circuit

# The qa register is 1 ancilla qubit.
# The qc register is n clock qubits.
# The qb register is m qubits for the b/x vectors.

qa = QuantumRegister(1, 'a')
qc = QuantumRegister(n, 'c')
qb = QuantumRegister(m, 'b')
qubits = [qubit for register in [qa, qc, qb] for qubit in register]
clbits = ClassicalRegister(1 + n + m)
circuit = QuantumCircuit(qa, qc, qb, clbits)
circuit.initialize(b/np.linalg.norm(b), qb)
circuit.h(qc)
for i, U in enumerate(U_matrices):
    Ugate = UnitaryGate(U, label=f"$U^{{{2**i}}}$").control(1)
    circuit.append(Ugate, [qc[i], *qb])
circuit.append(QFT(n).inverse(), qc)
maxλ = max(λ)
if args.scalingmode == "half":
    ƛ = [int(round(2**(n-1) * λi / maxλ)) for λi in λ] # scale so that maximum ƛ is 2^(n-1), i.e. will be binary 0.100...0.
else:
    ƛ = [int(round((2**n-1) * λi / maxλ)) for λi in λ] # scale so that maximum ƛ is (2^n-1)/2^n, i.e. will be binary 0.111...1.
minƛ = min(ƛ)

print(f"{ƛ=}")
print(f"{minƛ=}")
θ = [2 * np.arcsin(minƛ / ƛi) for ƛi in ƛ] # scale so that maximum θ is ArcSin[1]=π
bits = [f"{ƛi:0{n}b}" for ƛi in ƛ] # bit pattern for each λ, for C0 and C1 control bits of ancilla rotation
for i in range(len(λ)):
    RYi = RYGate(θ[i]).control(n, ctrl_state=bits[i])
    circuit.append(RYi, [*qc, qa[0]])
    if args.verbose:
        print(f"{i}:{λ[i]}:{ƛ[i]}:{bits[i]}:{θ[i]}")
circuit.append(QFT(n), qc)
for i, invU in enumerate(reversed(invU_matrices)):
    invUgate = UnitaryGate(invU, label=f"$U^{{{-2**(n-i-1)}}}$").control(1)
    circuit.append(invUgate, [qc[n-i-1], *qb])
circuit.barrier()
circuit.h(qc)
circuit.barrier()
circuit.measure(qubits, clbits)

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
total = sum(counts.values()) # sum of all counts
a1_total = sum(val for bits, val in counts.items() if bits.endswith("1")) # sum of counts when ancilla qubit is 1
a1_sum_ampls = sum(math.sqrt(val/a1_total) for bits, val in counts.items() if bits.endswith("1")) # sum of |ɑ| amplitude magnitude when ancilla qubit is 1

# Print the results
for bits, val in sorted(counts.items()):
    if bits.endswith("1"):
        print(f"{bits}\t{val}\t{val/a1_total:.{args.decimals}f}\t{math.sqrt(val/a1_total)/a1_sum_ampls:.{args.decimals}f}")
    else:
        print(f"{bits}\t{val}")

print(f"Prob(ancilla |0⟩) = {a1_total/total:.{args.decimals}f}")
