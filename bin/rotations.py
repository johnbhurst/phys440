#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-03-07

import jhqiskit
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from math import pi


qr = QuantumRegister(1, 'q')
cr = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qr, cr)

circuit.rx(pi/2, qr[0])
circuit.measure(qr, cr)

circuit.draw('mpl')

result = jhqiskit.run(circuit)
jhqiskit.print_result(result)
