#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-03-07

import jhqiskit
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister


qr = QuantumRegister(1, 'q')
cr = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(qr, cr)

circuit.h(qr[0])
circuit.measure(qr[0], cr[0])
circuit.measure(qr[0], cr[1])
circuit.h(qr[0])
circuit.measure(qr[0], cr[2])

circuit.draw('mpl')

result = jhqiskit.run(circuit)

print(result)
