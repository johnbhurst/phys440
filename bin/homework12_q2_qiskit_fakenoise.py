#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)

# See https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/fake_provider

import argparse
from math import pi
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeManilaV2, FakeKyoto, FakeOsaka
from qiskit_ibm_runtime.options import EnvironmentOptions, SamplerOptions
from qiskit.primitives import BackendSampler
from qiskit.providers.basic_provider import BasicProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='Homework 12 Q2: Noise from Qiskit fake providers.')
parser.add_argument('--provider', type=str, default='Simulator', help='Provider (Simulator, FakeManila, FakeKyoto, FakeOsaka), (default Simulator)')
parser.add_argument('--runs', type=int, default=1, help='Number of runs (default 1)')
args = parser.parse_args()

# NOTE: According to https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/fake_provider, we will get more up-to-date results
# using a backend from AerSimulator.from_backend(backend), which will have more up-to-date calibration results from the IBM Quantum systems.
# However, I tried this and the program seems to hang.
# I also saw some warnings like "UserWarning: The backend ibm_kyoto is currently paused."
# Therefore, at this time I am using only the static fake backends.
# Although these are not as accurate, they still demonstrate the noise differences between systems.

# service = QiskitRuntimeService()
# print("Getting backend")
# backend = service.get_backend('ibm_osaka')
# generate a simulator that mimics the real quantum system with the latest calibration results
# print("Getting simulator")
# backend_sim = AerSimulator.from_backend(backend)

def get_circuit(obs):
    q = QuantumRegister(2, 'q')
    c = ClassicalRegister(2, 'c')
    circuit = QuantumCircuit(q, c)
    # Prepare Bell state |𝚿⁻⟩ = 1/√2 (|01⟩ - |10⟩)
    circuit.h(q[0])
    circuit.cx(q[0], q[1])
    circuit.x(q[0])
    circuit.z(q[0])
    # Add the transformations for the observables
    if obs in ['apb', 'apbp']:
        circuit.h(q[0])
    circuit.ry(-pi/4, q[1])
    if obs in ['abp', 'apbp']:
        circuit.h(q[1])
    # Measure both qubits
    circuit.measure(q[0], c[0])
    circuit.measure(q[1], c[1])
    return circuit

def get_backend(backend):
    if backend == 'Simulator':
        return BasicProvider().get_backend('basic_simulator')
    elif backend == 'FakeManila':
        return FakeManilaV2()
    elif backend == 'FakeKyoto':
        return FakeKyoto()
    elif backend == 'FakeOsaka':
        return FakeOsaka()
    else:
        print("Provider must be one of Simulator, FakeManila, FakeKyoto, FakeOsaka")
        exit(1)

def run(obs, backend):
    circuit = get_circuit(obs)
    transpiled_circuit = transpile(circuit, backend)
    job = backend.run(transpiled_circuit)
    counts = job.result().get_counts()
    c00 = counts["00"]
    c01 = counts["01"]
    c10 = counts["10"]
    c11 = counts["11"]
    p00 = c00 / (c00 + c01 + c10 + c11)
    p01 = c01 / (c00 + c01 + c10 + c11)
    p10 = c10 / (c00 + c01 + c10 + c11)
    p11 = c11 / (c00 + c01 + c10 + c11)
    return p00 - p01 - p10 + p11

backend = get_backend(args.provider)

for i in range(args.runs):
    ab = run('ab', backend)
    abp = run('abp', backend)
    apb = run('apb', backend)
    apbp = run('apbp', backend)
    c = ab - abp + apb + apbp
    print(f"{i+1},{ab},{abp},{apb},{apbp},{c}")
