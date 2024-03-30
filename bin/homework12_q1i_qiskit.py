#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-03-24

# See https://docs.quantum.ibm.com/run/native-gates#native-gates-on-platform

import argparse
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.compiler import transpile
from qiskit.primitives import BackendSampler
from qiskit.providers.basic_provider import BasicProvider

parser = argparse.ArgumentParser(description='Homework 12 Q1(i): Bell states PhiPlus, PhiMinus, PsiPlus, PsiMinus.')
parser.add_argument('--phiplus', action='store_true', help='Create PhiPlus state')
parser.add_argument('--phiminus', action='store_true', help='Create PhiMinus state')
parser.add_argument('--psiplus', action='store_true', help='Create PsiPlus state')
parser.add_argument('--psiminus', action='store_true', help='Create PsiMinus state')
parser.add_argument('--shots', type=int, default=1024, help='Number of shots')
parser.add_argument('--transpile', type=str, default=None, help='Transpile to target architecture, e.g. "eagle"')
parser.add_argument('--filename', type=str, help='Filename for output')
args = parser.parse_args()

if not args.phiplus and not args.phiminus and not args.psiplus and not args.psiminus:
    print('Please specify one of --phiplus, --phiminus, --psiplus, --psiminus')
    exit(1)

transpile_basis_gates = {
    'heron': ['cz', 'rz', 'sx', 'x', 'id', 'reset', 'if_else', 'for_loop', 'switch_case', 'measure', 'delay'],
    'eagle': ['ecr', 'rz', 'sx', 'x', 'id', 'reset', 'if_else', 'for_loop', 'switch_case', 'measure', 'delay'],
    'falcon': ['cx', 'rz', 'sx', 'x', 'id', 'reset', 'if_else', 'for_loop', 'switch_case', 'measure', 'delay'],
}

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[1])
if args.psiplus or args.psiminus:
    circuit.x(qreg_q[0])
if args.phiminus or args.psiminus:
    circuit.z(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

if args.transpile:
    if args.transpile not in transpile_basis_gates:
        print(f"Unknown transpile target {args.transpile}; allowed values are {', '.join(list(transpile_basis_gates.keys()))}")
        exit(1)
    basis_gates = transpile_basis_gates[args.transpile]
    circuit = transpile(circuit, basis_gates=basis_gates)

if args.filename:
    with open(args.filename, 'w') as f:
        circuit.draw('mpl', filename=args.filename)

backend = BasicProvider().get_backend('basic_simulator')
sampler = BackendSampler(backend)
job = sampler.run(circuit, shots=args.shots)
result = job.result()
dists = {'{:02b}'.format(int(k)): v
         for k, v in result.quasi_dists[0].items()}
for k in sorted(dists.keys()):
    print(f'{k}: {dists[k]:.4f}')
