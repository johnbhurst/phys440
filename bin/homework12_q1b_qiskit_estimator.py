#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-04-13

# PHYS440: Homework 1+2 Q1(ii): X Correlator
# See https://learning.quantum.ibm.com/tutorial/chsh-inequality
# See https://docs.quantum.ibm.com/run/native-gates#native-gates-on-platform
# See https://docs.quantum.ibm.com/api/qiskit/qiskit.quantum_info.SparsePauliOp

import argparse
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import EstimatorV2 as Estimator, QiskitRuntimeService
from qiskit_ibm_runtime.options import EnvironmentOptions, EstimatorOptions
from qiskit.primitives import StatevectorEstimator
from qiskit.providers.basic_provider import BasicProvider
from qiskit.providers.jobstatus import JobStatus
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='Homework 12 Q1(ii): X Correlator.')
parser.add_argument('--filename', type=str, help='Filename for circuit diagram')
parser.add_argument('--shots', type=int, default=1024, help='Number of shots')
parser.add_argument('--run', action='store_true', help='Run on IBM Quantum')
parser.add_argument('--simulate', action='store_true', help='Run on Simulator')
parser.add_argument('--review', action='store_true', help='Review the job result')
parser.add_argument('job_id', type=str, nargs='?', help='Job ID')
args = parser.parse_args()

if (1 if args.run else 0) + (1 if args.simulate else 0) + (1 if args.review else 0) != 1:
    print('Please select either --run, --simulate or --review')
    exit(1)

# Define circuit for Bell state |Φ⁺⟩ = (|00⟩ + |11⟩) / √2.
chsh_circuit = QuantumCircuit(2)
chsh_circuit.h(0)
chsh_circuit.cx(0, 1)
# Define observable as 1 * X_1 * X_0.
observable = SparsePauliOp.from_list([("XX", 1)])

if args.run or args.review:
    service = QiskitRuntimeService(channel='ibm_quantum')

if args.run:
    backend = service.least_busy(operational=True, simulator=False)
    job_tags = ['homework12', 'xcorrelator', backend.name]
    options = EstimatorOptions(default_shots=args.shots, environment=EnvironmentOptions(job_tags=job_tags))
    estimator = Estimator(backend=backend, options=options)
elif args.simulate:
    backend = BasicProvider().get_backend('basic_simulator')
    estimator = StatevectorEstimator()

if args.run or args.simulate:
    target = backend.target
    pm = generate_preset_pass_manager(target=target, optimization_level=3)
    chsh_isa_circuit = pm.run(chsh_circuit)
    if args.filename:
        chsh_isa_circuit.draw(output='mpl', idle_wires=False, style='iqp', filename=args.filename)

    isa_observable = observable.apply_layout(layout=chsh_isa_circuit.layout)
    pub = (chsh_isa_circuit, [[isa_observable]])
    job = estimator.run(pubs=[pub])

if args.run:
    print(f"Job ID is {job.job_id()}")
elif args.simulate:
    job_result = job.result()
    est = job_result[0].data.evs[0]
    print(est)

if args.review:
    job = service.job(args.job_id)
    if job.status() == JobStatus.DONE:
        job_result = job.result()
        for idx, pub_result in enumerate(job_result):
            if "evs" in dir(pub_result.data):
                print(f"Estimate data for pub {idx}: {pub_result.data.evs}")
            else:
                print(f"I don't recognize the data type for pub {idx}: {dir(pub_result.data)}")
    else:
        print(f"Status: {job.status()}")
