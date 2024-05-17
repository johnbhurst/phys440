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
from qiskit.circuit.library import QFT
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='PHYS440 Homework 3 Q2: Quantum Phase Estimation.')
parser.add_argument("--operator", type=str, default="Z", help="Operator (Z, Y), (default Z)")
parser.add_argument("--eigenvector", type=str, default="e0", help="Eigenvector (e0, e1), (default e0)")
parser.add_argument("--qft", action="store_true", help="Apply QFT builtin")
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
args = parser.parse_args()

assert args.operator in ["Z", "Y"], "Invalid operator: Must be Z, Y"
assert args.eigenvector in ["e0", "e1"], "Invalid eigenvector: Must be e0, e1"

qubits = QuantumRegister(3)
clbits = ClassicalRegister(2)
circuit = QuantumCircuit(qubits, clbits)

# Setup:
if args.operator == "Z":
    if args.eigenvector == "e0":
        circuit.x(0)
else:
    if args.eigenvector == "e0":
        circuit.rx(math.pi/2, 0)
    else:
        circuit.rx(-math.pi/2, 0)
circuit.h(1)
circuit.h(2)
if args.operator == "Z":
    circuit.cz(1, 0)
else:
    circuit.cy(1, 0)

# 2-qubit QFT, either using builtin or manual implementation:
if args.qft:
    circuit.append(QFT(2).inverse(), qubits[1:3])
else:
    circuit.h(2)
    circuit.cp(-math.pi/2, 1, 2)
    circuit.h(1)
    circuit.swap(1, 2)

# measure:
circuit.measure(qubits[1:], clbits)

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
