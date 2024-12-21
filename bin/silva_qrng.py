#!/usr/bin/env python
# Quantum Random Number Generator from "Quantum Computing by Practice" by Vladimir Silva, 2nd Ed, Apress 2024

import argparse
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

parser = argparse.ArgumentParser(description="Generate random numbers using a quantum circuit.")
parser.add_argument("--size", type=int, default=100, help="Number of random numbers to generate.")
parser.add_argument("--binfile", type=str, help="Binary file to write random numbers to.")
args = parser.parse_args()

def qrng(n):
    quantum_r = QuantumRegister(n, "qr")
    classical_r = ClassicalRegister(n, "cr")
    circuit = QuantumCircuit(quantum_r, classical_r, name="QRNG")
    for i in range(n):
        circuit.h(quantum_r[i])
    for i in range(n):
        circuit.measure(quantum_r[i], classical_r[i])
    backend = AerSimulator()
    isa_circuit = transpile(circuit, backend)
    sampler = Sampler(backend)
    shots = 1024
    job = sampler.run([isa_circuit], shots=shots)
    result = job.result()
    counts = result[0].data.cr.get_counts()
    bits = ""
    for v in counts.values():
        if v > shots/(2**n):
            bits += "1"
        else:
            bits += "0"
    return int(bits, 2)

size = args.size
qubits = 3
numbers = []
for i in range(size):
    n = qrng(qubits)
    numbers.append(n)

if args.binfile:
    with open(args.binfile, "wb") as f:
        for n in numbers:
            f.write(n.to_bytes(1, "big"))
else:
    print(str(numbers).replace('[','').replace(']',''))
