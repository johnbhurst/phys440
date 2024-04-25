#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)

# See https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/fake_provider

import argparse
from math import sqrt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2
from qiskit_ibm_runtime.options import EstimatorOptions
from qiskit.primitives import StatevectorEstimator
from qiskit.providers.basic_provider import BasicProvider
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='Homework 12 Q2: Noise from Qiskit fake providers (using Estimator).')
parser.add_argument('--provider', type=str, default='basic_simulator', help='Provider (basic_simulator, fake_manila, fake_kyoto, fake_osaka etc), (default basic_simulator)')
parser.add_argument('--runs', type=int, default=1, help='Number of runs (default 1)')
parser.add_argument('--shots', type=int, default=1024, help='Number of shots (default 1024)')
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

# options = EstimatorOptions(default_shots=args.shots)
if args.provider == 'basic_simulator':
    backend = BasicProvider().get_backend('basic_simulator')
    estimator = StatevectorEstimator()
else:
    backends = FakeProviderForBackendV2().backends()
    backend = next(iter([backend for backend in backends if backend.name == args.provider]), None)
    if not backend:
        print("Provider must be one of basic_simulator, fake_manila, fake_kyoto, fake_osaka etc")
        exit(1)
    estimator = Estimator(backend=backend)
    # estimator = Estimator(backend=backend, options=options)

# Prepare Bell state |𝚿⁻⟩ = 1/√2 (|01⟩ - |10⟩)
circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.x(0)
circuit.z(0)
# transpiled_circuit = transpile(circuit, backend)

# AB = Z₀ x 1/√2 (X₁+Z₁)
#    = 1/√2 (X₁Z₀ + Z₁Z₀)
observable_ab = SparsePauliOp.from_list([("XZ", 1/sqrt(2)), ("ZZ", 1/sqrt(2))])
# AB' = Z₀ x 1/√2 (X₁-Z₁)
#     = 1/√2 (X₁Z₀ - Z₁Z₀)
observable_abp = SparsePauliOp.from_list([("XZ", 1/sqrt(2)), ("ZZ", -1/sqrt(2))])
# A'B = X₀ x 1/√2 (X₁+Z₁)
#     = 1/√2 (X₁X₀ + Z₁X₀)
observable_apb = SparsePauliOp.from_list([("XX", 1/sqrt(2)), ("ZX", 1/sqrt(2))])
# A'B' = X₀ x 1/√2 (X₁-Z₁)
#      = 1/√2 (X₁X₀ - Z₁X₀)
observable_apbp = SparsePauliOp.from_list([("XX", 1/sqrt(2)), ("ZX", -1/sqrt(2))])
# C = AB - AB' + A'B + A'B'
#   = 1/√2 (X₁Z₀ + Z₁Z₀) - 1/√2 (X₁Z₀ - Z₁Z₀) + 1/√2 (X₁X₀ + Z₁X₀) + 1/√2 (X₁X₀ - Z₁X₀)
#   = √2 Z₁Z₀ + √2 X₁X₀
observable_c = SparsePauliOp.from_list([("ZZ", sqrt(2)), ("XX", sqrt(2))])

target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
transpiled_circuit = pm.run(circuit)
isa_observable_ab = observable_ab.apply_layout(layout=transpiled_circuit.layout)
isa_observable_abp = observable_abp.apply_layout(layout=transpiled_circuit.layout)
isa_observable_apb = observable_apb.apply_layout(layout=transpiled_circuit.layout)
isa_observable_apbp = observable_apbp.apply_layout(layout=transpiled_circuit.layout)
isa_observable_c = observable_c.apply_layout(layout=transpiled_circuit.layout)
pub = (transpiled_circuit, [[isa_observable_ab, isa_observable_abp, isa_observable_apb, isa_observable_apbp, isa_observable_c]])

for i in range(args.runs):
    est = estimator.run(pubs=[pub]).result()[0].data.evs[0]
    print(",".join(map(str, est)))
