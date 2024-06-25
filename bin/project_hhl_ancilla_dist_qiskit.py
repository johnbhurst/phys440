#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-06-21

import argparse
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import random
import scipy
import sys
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2 as FakeProvider
from qiskit.circuit.library import QFT, RYGate, UnitaryGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='PHYS440 Project: HHL ancilla |0> probability distribution.')
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--runs", type=int, default=100, help="Number of runs for frequency distribution")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots in each run")
parser.add_argument("--size", type=int, default=4, help="Size of matrix")
parser.add_argument("--clockqubits", type=int, default=3, help="Number of clock qubits")
parser.add_argument("--decimals", type=int, default=4, help="Number of decimal places")
parser.add_argument("--scalingmode", type=str, default="half", help="Eigenvalue scaling mode (half, full) (default half)")
parser.add_argument("--verbose", action="store_true", help="Verbose output")
parser.add_argument("--filename", type=str, help="Filename for histogram")
args = parser.parse_args()

def run(A, b, m, n):
    x = np.linalg.solve(A, b) # actual solution vector x
    xabssum = sum(abs(x))     # sum of absolute values of x
    xp = abs(x) / xabssum          # normalized x
    actx = {}                 # dict of bit patterns to actual x values
    for i, xi in enumerate(xp):
        bits = f"{i:0{m}b}" + "0" * n + "1"
        actx[bits] = xi

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

    t = π / max(λ)
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
    if args.scalingmode == "half":
        ƛ = [int(round(2**n * t * λi / (2 * π))) for λi in λ] # scale so that maximum ƛ is 2^(n-1), i.e. will be binary 0.100...0.
    else:
        ƛ = [int(round((2**n-1) * t * λi / π)) for λi in λ] # scale so that maximum ƛ is (2^n-1)/2^n, i.e. will be binary 0.111...1.

    θ = [2 * np.arcsin(min(ƛ) / ƛi) for ƛi in ƛ] # scale so that maximum θ is ArcSin[1]=π
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
    if args.provider == 'aer':
        backend = AerSimulator()
    else:
        backend = next(iter([backend for backend in FakeProvider().backends() if backend.name == args.provider]), None)

    sampler = Sampler(backend)

    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    job = sampler.run([isa_circuit], shots=args.shots)
    result = job.result()
    # counts = result[0].data.c0.get_counts()
    counts = list(result[0].data.values())[0].get_counts()
    total = sum(counts.values()) # sum of all counts
    a1_total = sum(val for bits, val in counts.items() if bits.endswith("1")) # sum of counts when ancilla qubit is 1
    a1_sum_ampls = sum(math.sqrt(val/a1_total) for bits, val in counts.items() if bits.endswith("1")) # sum of |ɑ| amplitude magnitude when ancilla qubit is 1
    ancilla_prob = a1_total / total
    return ancilla_prob


π = math.pi
size = args.size
m = int(math.log2(size))
n = args.clockqubits
H = scipy.linalg.hadamard(size)

data = []
for run_num in range(args.runs):
    l = random.sample(list(range(1, int(2**(n-1)))), size-1) # random list of m-1 integers from 1 to 2^(n-1)-1
    l = l + [int(2**(n-1))] # add 2^(n-1) to the list
    random.shuffle(l) # shuffle the list
    L = np.diag(l) # diagonal matrix L
    A = H @ L @ H.T # matrix A
    # choose m random floats from 1 to 10 for b
    b = np.array([random.uniform(1, 10) for _ in range(size)])
    data.append(run(A, b, m, n))

df = pd.DataFrame(data, columns=['Frequency'])

# Plotting the histogram
df.plot.hist(bins=20, range=(0, 1), rwidth=0.9, legend=False)
# plt.title('Histogram of Ancilla Qubit Frequencies')
plt.xlabel('Probability')
plt.ylabel('Counts')
plt.grid(axis='y', alpha=0.75)

# Display the plot
if args.filename:
    plt.savefig(args.filename)
else:
    plt.show()
