#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-03-07

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.providers.basic_provider import BasicProvider
from qiskit.primitives import BackendSampler

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[0], creg_c[1])
circuit.h(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[2])

circuit.draw('mpl')

backend = BasicProvider().get_backend('basic_simulator')
sampler = BackendSampler(backend)
job = sampler.run(circuit, shots=1000)
result = job.result()

print(result)
