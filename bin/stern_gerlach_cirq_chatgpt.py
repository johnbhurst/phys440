#!/usr/bin/env python

import cirq

# Define a quantum circuit
circuit = cirq.Circuit()

# Get a qubit and a circuit
q = cirq.LineQubit(0)

# Apply Hadamard gate to put the qubit in superposition (similar to creating an undefined spin)
circuit.append(cirq.H(q))

# Measure the qubit (analogous to observing the spin direction)
circuit.append(cirq.measure(q, key='result'))

# Print the circuit
print("Circuit:")
print(circuit)

# Simulate the circuit
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=100)
print("Measurement results:")
print(result.histogram(key='result'))

