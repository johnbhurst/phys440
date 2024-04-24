#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-04-23

# See https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/qiskit_ibm_runtime.fake_provider.FakeProviderForBackendV2

from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2

backends = FakeProviderForBackendV2().backends()
for backend in backends:
    print(f"{backend.name}: {type(backend)}")

