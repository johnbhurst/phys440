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


def print_result(result):
    dists = result.quasi_dists
    assert(len(dists) == 1)
    dists = {format(int(k), '010b'): v for k, v in dists[0].items()}
    for k in sorted(dists.keys()):
        print(f'{k}: {dists[k]:.4f}')
