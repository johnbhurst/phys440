#!/usr/bin/env python
# See https://docs.quantum.ibm.com/run/native-gates

from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(channel="ibm_quantum")

for backend in service.backends():
    config = backend.configuration()
    if "simulator" in config.backend_name:
        continue
    print(f"Backend: {config.backend_name}")
    print(f"    Processor type: {config.processor_type}")
    print(f"    Supported instructions:")
    for instruction in config.supported_instructions:
        print(f"        {instruction}")
    print()