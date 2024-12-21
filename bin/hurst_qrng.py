#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-12-22

# Improved Quantum Random Number Generator from "Quantum Computing by Practice" by Vladimir Silva, 2nd Ed, Apress 2024

import argparse
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

parser = argparse.ArgumentParser(description="Generate random numbers using a quantum circuit.")
parser.add_argument("--size", type=int, default=100, help="Number of random numbers to generate.")
parser.add_argument("--binfile", type=str, help="Binary file to write random numbers to.")
args = parser.parse_args()

def qrng(n):
    qr = QuantumRegister(n, "qr")
    cr = ClassicalRegister(n, "cr")
    circuit = QuantumCircuit(qr, cr, name="QRNG")
    circuit.h(qr)
    circuit.measure(qr, cr)
    backend = AerSimulator()
    sampler = Sampler(backend)
    job = sampler.run([circuit], shots=1)
    result = job.result()
    counts = result[0].data.cr.get_counts()
    return next(int(k, 2) for k, v in counts.items() if v == 1)

size = args.size
qubits = 8
numbers = [qrng(qubits) for i in range(size)]

if args.binfile:
    with open(args.binfile, "wb") as f:
        for n in numbers:
            f.write(n.to_bytes(1, "big"))
else:
    print(", ".join([str(n) for n in numbers]))
