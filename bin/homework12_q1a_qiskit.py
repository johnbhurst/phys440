#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-03-24

# PHYS440: Homework 1+2 Q1(i): Bell states PhiPlus, PhiMinus, PsiPlus, PsiMinus
# See https://docs.quantum.ibm.com/run/native-gates#native-gates-on-platform

import argparse
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime.options import EnvironmentOptions, SamplerOptions
from qiskit.compiler import transpile
from qiskit.primitives import BackendSampler
from qiskit.providers.basic_provider import BasicProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

transpile_basis_gates = {
    'heron': ['cz', 'rz', 'sx', 'x', 'id', 'reset', 'if_else', 'for_loop', 'switch_case', 'measure', 'delay'],
    'eagle': ['ecr', 'rz', 'sx', 'x', 'id', 'reset', 'if_else', 'for_loop', 'switch_case', 'measure', 'delay'],
    'falcon': ['cx', 'rz', 'sx', 'x', 'id', 'reset', 'if_else', 'for_loop', 'switch_case', 'measure', 'delay'],
}
transpile_architectures = list(transpile_basis_gates.keys())

# Configure, parse and validate command line arguments
parser = argparse.ArgumentParser(description='Homework 12 Q1(i): Bell states PhiPlus, PhiMinus, PsiPlus, PsiMinus.')
parser.add_argument('--state', type=str, default='phiplus', help='State to create (phiplus, phiminus, psiplus, psiminus)')
parser.add_argument('--shots', type=int, default=1024, help='Number of shots')
parser.add_argument('--transpile', type=str, default=None, help=f"Transpile to target architecture ({', '.join(transpile_architectures)}")
parser.add_argument('--filename', type=str, help='Filename for circuit diagram')
parser.add_argument('--format', type=str, default='mpl', help='Output format (mpl, latex)')
parser.add_argument('--simulate', action='store_true', help='Simulate the circuit')
parser.add_argument('--run', action='store_true', help='Run the circuit on IBM Quantum')
parser.add_argument('--pass-manager', action='store_true', help='Run pass manager to transform circuit for backend architecture')
parser.add_argument('--optimization-level', type=int, default=1, help='Optimization level for pass manager')
args = parser.parse_args()
if (args.state != "phiplus" and args.state != "phiminus" and
    args.state != "psiplus" and args.state != "psiminus"):
    print('State must be one of phiplus, phiminus, psiplus, psiminus')
    exit(1)
if (args.transpile is not None and args.transpile not in transpile_architectures):
    print(f"Transpile target must be one of {', '.join(transpile_architectures)}")
    exit(1)
if (args.format is not None and args.format != 'mpl' and args.format != 'latex'):
    print('Format must be one of mpl, latex')
    exit(1)

# Build the circuit
qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
circuit.h(qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[1])
if args.state == "psiplus" or args.state == "psiminus":
    circuit.x(qreg_q[0])
if args.state == "phiminus" or args.state == "psiminus":
    circuit.z(qreg_q[0])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

# Transpile if requested
# Note: Although this transpilation generates circuits using supported gates for the target architecture,
# the circuits are still not compatible with the rarget instruction set architectures, due to qubit allocation.
# Use the --pass-manager option when running circuits on IBM Quantum.
if args.transpile:
    circuit = transpile(circuit, basis_gates=transpile_basis_gates[args.transpile])

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
    job_tags = ['homework12', 'bell', args.state, backend.name]
    if args.transpile:
        job_tags.append(args.transpile)
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
