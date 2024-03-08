#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-03-09

import jhqiskit
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from math import pi


qr = QuantumRegister(10, 'q')
cr = ClassicalRegister(10, 'c')
circuit = QuantumCircuit(qr, cr)

circuit.rx(pi/2, qr[0])
circuit.rx(pi/2, qr[1])
circuit.rx(pi/2, qr[2])
circuit.rx(pi/2, qr[3])
circuit.rx(pi/2, qr[4])
circuit.rx(pi/2, qr[5])
circuit.rx(pi/2, qr[6])
circuit.rx(pi/2, qr[7])
circuit.rx(pi/2, qr[8])
circuit.rx(pi/2, qr[9])

circuit.measure(qr, cr)

circuit.draw('mpl')

result = jhqiskit.run(circuit)
jhqiskit.print_result(result)
