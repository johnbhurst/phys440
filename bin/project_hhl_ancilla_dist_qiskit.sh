 #!/usr/bin/env bash
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-06-21

# echo "2x2, 2 clock qubits"
# bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=2 --clockqubits=2 --filename=ancilla_frequency_dist_2x2b2.png
# echo "2x2, 3 clock qubits"
# bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=2 --clockqubits=3 --filename=ancilla_frequency_dist_2x2b3.png
# echo "2x2, 4 clock qubits"
# bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=2 --clockqubits=4 --filename=ancilla_frequency_dist_2x2b4.png
# echo "2x2, 5 clock qubits"
# bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=2 --clockqubits=5 --filename=ancilla_frequency_dist_2x2b5.png
echo "2x2, 6 clock qubits"
bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=2 --clockqubits=6 --filename=ancilla_frequency_dist_2x2b6.png

echo "4x4, 3 clock qubits"
bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=4 --clockqubits=3 --filename=ancilla_frequency_dist_4x4b3.png
echo "4x4, 4 clock qubits"
bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=4 --clockqubits=4 --filename=ancilla_frequency_dist_4x4b4.png
echo "4x4, 5 clock qubits"
bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=4 --clockqubits=5 --filename=ancilla_frequency_dist_4x4b5.png
echo "4x4, 6 clock qubits"
bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=4 --clockqubits=6 --filename=ancilla_frequency_dist_4x4b6.png

echo "8x8, 4 clock qubits"
bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=8 --clockqubits=4 --filename=ancilla_frequency_dist_8x8b4.png
echo "8x8, 5 clock qubits"
bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=8 --clockqubits=5 --filename=ancilla_frequency_dist_8x8b5.png
echo "8x8, 6 clock qubits"
bin/project_hhl_ancilla_dist_qiskit.py --runs=1000 --size=8 --clockqubits=6 --filename=ancilla_frequency_dist_8x8b6.png
