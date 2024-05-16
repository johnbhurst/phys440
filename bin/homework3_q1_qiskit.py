#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-05-13

import argparse
import math
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2 as FakeProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='Homework 3 Q1: Quantum teleportation.')
parser.add_argument('--provider', type=str, default='aer', help='Provider (aer, fake_manila, fake_kyoto, etc), (default aer)')
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--theta", type=str, default="0.0", help="Theta angle as a fraction of pi, e.g., 'pi/2'")
parser.add_argument("--phi", type=str, default="0.0", help="Phi angle as a fraction of pi, e.g., '-pi/4'")
parser.add_argument("--realign", action="store_true", help="Realign qubit 2 to measure as original state of qubit 0")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
args = parser.parse_args()

def safe_eval(expr):
    allowed_names = {"pi": math.pi}
    return eval(expr, {"__builtins__": None}, allowed_names)

theta = safe_eval(args.theta)
phi = safe_eval(args.phi)

qubits = QuantumRegister(3)
clbits = ClassicalRegister(3)
circuit = QuantumCircuit(qubits, clbits)
(q0, q1, q2) = qubits
(c0, c1, c2) = clbits

circuit.ry(theta, q0)
circuit.rz(phi, q0)
circuit.h(q1)
circuit.cx(q1, q2)
circuit.cx(q0, q1)
circuit.h(q0)
circuit.measure(q0, c0)
circuit.measure(q1, c1)
circuit.x(q2).c_if(c1, 1)
circuit.z(q2).c_if(c0, 1)
if args.realign:
    circuit.rz(-phi, q2)
    circuit.ry(-theta, q2)
circuit.measure(q2, c2)

if args.provider == 'aer':
    backend = AerSimulator()
else:
    backend = next(iter([backend for backend in FakeProvider().backends() if backend.name == args.provider]), None)

sampler = Sampler(backend)

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(circuit)

if args.filename:
    isa_circuit.draw(output="mpl", style='iqp', idle_wires=False, cregbundle=False, filename=args.filename)

job = sampler.run([isa_circuit], shots=args.shots)
result = job.result()
counts = result[0].data.c0.get_counts()
count0 = counts.get("000", 0) + counts.get("001", 0) + counts.get("010", 0) + counts.get("011", 0)
count1 = counts.get("100", 0) + counts.get("101", 0) + counts.get("110", 0) + counts.get("111", 0)

print(count0, count1)