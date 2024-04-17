#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-03-24

import argparse
import cirq
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Homework 12 Q1(i): Bell states PhiPlus, PhiMinus, PsiPlus, PsiMinus.')
parser.add_argument('--phiplus', action='store_true', help='Create PhiPlus state')
parser.add_argument('--phiminus', action='store_true', help='Create PhiMinus state')
parser.add_argument('--psiplus', action='store_true', help='Create PsiPlus state')
parser.add_argument('--psiminus', action='store_true', help='Create PsiMinus state')
parser.add_argument('--shots', type=int, default=1024, help='Number of shots')
parser.add_argument('--filename', type=str, help='Filename for output')
args = parser.parse_args()

if not args.phiplus and not args.phiminus and not args.psiplus and not args.psiminus:
    print('Please specify one of --phiplus, --phiminus, --psiplus, --psiminus')
    exit(1)

q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit()
circuit.append(cirq.H(q0))
circuit.append(cirq.CNOT(q0, q1))
if args.psiplus or args.psiminus:
    circuit.append(cirq.X(q0))
if args.phiminus or args.psiminus:
    circuit.append(cirq.Z(q0))
print(circuit)

simulator = cirq.Simulator()
result = simulator.simulate(circuit)
print(result)

circuit.append(cirq.measure(q0, q1, key='result'))
samples = simulator.run(circuit, repetitions=args.shots)
binary_labels = [bin(x)[2:].zfill(2) for x in range(4)]
cirq.plot_state_histogram(samples, plt.subplot(), xlabel = 'measurement state', ylabel = 'count', tick_label=binary_labels)
if args.filename:
    plt.savefig(args.filename)
else:
    plt.show()

