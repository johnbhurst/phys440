#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-05-18

# Demonstrate bit order for QisKit

import argparse
import math
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2 as FakeProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import Operator

parser = argparse.ArgumentParser(description='PHYS440 Homework 3 Q2: Quantum Phase Estimation.')
parser.add_argument("--bits", type=int, default=3, help="Number of bits (default 3)")
parser.add_argument("--bit", type=int, default=0, help="Bit to set (default 0)")
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
args = parser.parse_args()

qubits = QuantumRegister(args.bits)
clbits = ClassicalRegister(args.bits)
circuit = QuantumCircuit(qubits, clbits)

# circuit.x(qubits[args.bit])
circuit.x(args.bit)

circuit.measure(qubits, clbits)

if args.filename:
    circuit.draw(output='mpl', filename=args.filename)

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

