#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
#

# PHYS440: Homework 1+2 Q2: CHSH Inequality
# See https://learning.quantum.ibm.com/tutorial/chsh-inequality
# See https://docs.quantum.ibm.com/run/native-gates#native-gates-on-platform

import argparse
from math import pi
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime.options import EnvironmentOptions, SamplerOptions
from qiskit.primitives import BackendSampler
from qiskit.providers.basic_provider import BasicProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Configure, parse and validate command line arguments
parser = argparse.ArgumentParser(description='Homework 12 Q2: CHSH Inequality.')
parser.add_argument('--obs', type=str, default='ab', help="Observations (ab=AB, apb=AB', apb=A'B, apbp=A'B')")
parser.add_argument('--shots', type=int, default=1024, help='Number of shots')
parser.add_argument('--filename', type=str, help='Filename for circuit diagram')
parser.add_argument('--format', type=str, default='mpl', help='Output format (mpl, latex)')
parser.add_argument('--simulate', action='store_true', help='Simulate the circuit')
parser.add_argument('--run', action='store_true', help='Run the circuit on IBM Quantum')
parser.add_argument('--pass-manager', action='store_true', help='Run pass manager to transform circuit for backend architecture')
parser.add_argument('--optimization-level', type=int, default=1, help='Optimization level for pass manager')
args = parser.parse_args()
if not args.obs in ['ab', 'abp', 'apb', 'apbp']:
    print("Observations must be one of ab (for AB), abp (AB'), apb (A'B), apbp (A'B')")
    exit(1)
if (args.format is not None and args.format != 'mpl' and args.format != 'latex'):
    print('Format must be one of mpl, latex')
    exit(1)

# Build the circuit
q = QuantumRegister(2, 'q')
c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(q, c)
# Prepare Bell state |𝚿⁻⟩ = 1/√2 (|01⟩ - |10⟩)
circuit.h(q[0])
circuit.cx(q[0], q[1])
circuit.x(q[0])
circuit.z(q[0])
# Add the transformations for the observables
if args.obs in ['apb', 'apbp']:
    circuit.h(q[0])
circuit.ry(-pi/4, q[1])
if args.obs in ['abp', 'apbp']:
    circuit.h(q[1])
# Measure both qubits
circuit.measure(q[0], c[0])
circuit.measure(q[1], c[1])

# Run the circuit in the local simulator if requested
if args.simulate:
    backend = BasicProvider().get_backend('basic_simulator')
    sampler = BackendSampler(backend)

    job = sampler.run([circuit])
    result = job.result()
    dists = {'{:02b}'.format(int(k)): v for k, v in result.quasi_dists[0].items()}
    for k in sorted(dists.keys()):
        print(f'{k}: {dists[k]:.4f}')

# Run the circuit on IBM Quantum if requested
if args.run:
    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False)
    job_tags = ['homework12', 'chsh', args.obs, backend.name]
    options = SamplerOptions(default_shots=args.shots, environment=EnvironmentOptions(job_tags=job_tags))
    sampler = Sampler(backend=backend, options=options)

    if args.pass_manager:
        pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=args.optimization_level)
        circuit = pass_manager.run(circuit)
    job = sampler.run([circuit])
    print(f"Job ID is {job.job_id()}")

# Draw the circuit if requested
if args.filename:
    circuit.draw(args.format, filename=args.filename)
