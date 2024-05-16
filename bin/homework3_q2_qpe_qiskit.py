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
parser.add_argument("--operator", type=str, default="Z", help="Operator (X, Y, Z), (default Z)")
parser.add_argument("--eigenvector", type=str, default="1", help="Eigenvector (0, 1), (default 1)")
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
args = parser.parse_args()

qubits = QuantumRegister(3)
clbits = ClassicalRegister(3)
circuit = QuantumCircuit(qubits, clbits)
(q0, q1, q2) = qubits
(c0, c1, c2) = clbits

# Setup:
if args.operator == "Z":
    if args.eigenvector == "1":
        circuit.x(q0)
elif args.operator == "X":
    raise NotImplementedError("X operator not implemented")
elif args.operator == "Y":
    if args.eigenvector == "0":
        circuit.rx(math.pi/2, q0)
    else:
        circuit.rx(-math.pi/2, q0)
else:
    raise ValueError("Invalid operator: Must be X, Y, or Z")
circuit.h(q1)
circuit.h(q2)
if args.operator == "Z":
    circuit.cz(q1, q0)
elif args.operator == "X":
    circuit.cx(q1, q0)
elif args.operator == "Y":
    circuit.cy(q1, q0)
else:
    raise ValueError("Invalid operator: Must be X, Y, or Z")

# 2-qubit QFT:
circuit.h(q2)
circuit.cp(-math.pi/2, q1, q2)
circuit.h(q1)
# circuit.swap(q1, q2) #TODO: swap to get qubit ordering that makes results easier to interpret

# measure:
circuit.measure(q1, c1)
circuit.measure(q2, c2)

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
print(counts)
