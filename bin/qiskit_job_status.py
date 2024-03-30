#!/usr/bin/env python
# adapted from code displayed on IBM Quantum Platform console
# John Hurst, 2024-03-31

import argparse
from qiskit.providers.jobstatus import JobStatus
from qiskit_ibm_runtime import QiskitRuntimeService

parser = argparse.ArgumentParser(description='Get Qiskit job status.')
parser.add_argument('job_id', type=str, help='Job ID')

args = parser.parse_args()

service = QiskitRuntimeService(channel='ibm_quantum')
job = service.job(args.job_id)

if job.status() == JobStatus.DONE:
    job_result = job.result()

    for idx, pub_result in enumerate(job_result):
        print(f"Sample data for pub {idx}: {pub_result.data.meas.get_counts()}")

else:
    print(job.status())