#!/usr/bin/env python

import cirq

qubit = cirq.NamedQubit('q')
circuit = cirq.Circuit()

circuit.append(cirq.H(qubit))  # Superposition
circuit.append(cirq.rz(0.5)(qubit))  # Simulate magnetic field
circuit.append(cirq.measure(qubit))

# Simulation
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)
print(result.histogram(key='q'))



