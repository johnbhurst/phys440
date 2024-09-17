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
parser.add_argument("--operator", type=str, default="Z", help="Operator (Z, Y, RX), (default Z)")
parser.add_argument("--theta", type=str, default="pi/2", help="Theta for RX operator (default 'pi/2')")
parser.add_argument("--eigenvector", type=str, default="e0", help="Eigenvector (e0, e1), (default e0)")
parser.add_argument("--bits", type=int, default=2, help="Number of bits of accuracy (default 2)")
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
args = parser.parse_args()

assert args.operator in ["Z", "Y", "RX"], "Invalid operator: Must be Z, Y, RX"
assert args.eigenvector in ["e0", "e1"], "Invalid eigenvector: Must be e0, e1"

def safe_eval(expr):
    allowed_names = {"pi": math.pi}
    return eval(expr, {"__builtins__": None}, allowed_names)

theta = safe_eval(args.theta)

# let n = args.bits, the number of bits for output accuracy.
# we assign qubits:
# qubit 0 is the input qubit.
# qubits 1:n are the output qubits.
input_qubit = 0
n = args.bits

qubits = QuantumRegister(n+1)
clbits = ClassicalRegister(n)
circuit = QuantumCircuit(qubits, clbits)

# Setup input qubit:
if args.operator == "Z":
    if args.eigenvector == "e0":
        circuit.x(input_qubit)
elif args.operator == "Y":
    if args.eigenvector == "e0":
        circuit.rx(math.pi/2, input_qubit)
    else:
        circuit.rx(-math.pi/2, input_qubit)
else:
    if args.eigenvector == "e0":
        circuit.ry(math.pi/2, input_qubit)
    else:
        circuit.ry(-math.pi/2, input_qubit)

# Prepare input for QFT:
for i in range(n):
    circuit.h(i+1)
for i in range(n):
    if args.operator == "Z" and n-i == 1:
        circuit.cz(n-i, input_qubit)
    elif args.operator == "Y" and n-i == 1:
        circuit.cy(n-i, input_qubit)
    elif args.operator == "RX":
        circuit.crx(theta*(2**(n-i-1)), n-i, input_qubit)

# QFT:
circuit.append(QFT(n).inverse(), qubits[1:])

# Measure:
circuit.measure(qubits[1:], clbits)

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
for k, v in counts.items():
    print(f"{k}: {v}")
