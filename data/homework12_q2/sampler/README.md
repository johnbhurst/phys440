# CHSH C estimate with different IBM Quantum providers

The images in this folder show the distribution of estimates of $C = <AB> - <AB'> + <A'B> + <A'B'>$ for the CHSH inequality in the homework assignment.

The estimates were made using the Qiskit Sampler feature, using a separate circuit for each combination of observables $A$, $B$, $A'$, and $B'$.

The estimates were done using the basic simulator provider, and the fake providers for each of 55 real IBM Quantum systems.

For each provider, 100 runs were done, each using 1,024 shots. The plots show the distribution of the estimated $C$ over the 100 runs on each provider.

