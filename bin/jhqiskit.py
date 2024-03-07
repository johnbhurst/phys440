# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-03-07

from qiskit.providers.basic_provider import BasicProvider
from qiskit.primitives import BackendSampler


def run(circuit, shots=1024):
    backend = BasicProvider().get_backend('basic_simulator')
    sampler = BackendSampler(backend)
    job = sampler.run(circuit, shots=shots)
    return job.result()

