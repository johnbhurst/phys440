#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-05-17

# Quantum Phase Estimation for eigenvalue of Pauli Z matrix
# See Hiu Yung Wong 2024 "Introduction to Quantum Computing: From a Layperson to a Programmer in 30 Steps"

import argparse
import math
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2 as FakeProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import Operator

parser = argparse.ArgumentParser(description='PHYS440 Homework 3 Q2: Quantum Phase Estimation.')
parser.add_argument("--operator", type=str, default="Z", help="Operator (Z, Y, RX), (default Z)")
parser.add_argument("--eigenvector", type=str, default="e0", help="Eigenvector (e0, e1), (default e0)")
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
args = parser.parse_args()

qubits = QuantumRegister(3)
clbits = ClassicalRegister(2)
circuit = QuantumCircuit(qubits, clbits)

# Setup:
if args.operator == "Z":
    if args.eigenvector == "e1":
        circuit.x(2)
elif args.operator == "Y":
    if args.eigenvector == "e0":
        circuit.rx(math.pi/2, 2)
    else:
        circuit.rx(-math.pi/2, 2)
else:
    raise ValueError("Invalid operator: Must be Z, Y, or RX")
circuit.h(1)
circuit.h(0)
if args.operator == "Z":
    circuit.cz(1, 2)
elif args.operator == "Y":
    circuit.cy(1, 2)
else:
    raise ValueError("Invalid operator: Must be Z, Y, or RX")

# 2-qubit QFT:
circuit.h(0)
circuit.cp(-math.pi/2, 1, 0)
circuit.h(1)
circuit.swap(0, 1)

# measure:
circuit.measure(1, 1)
circuit.measure(0, 0)

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
for k, v in counts.items():
    print(f"{k}: {v}")
