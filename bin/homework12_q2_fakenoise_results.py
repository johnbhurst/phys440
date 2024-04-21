#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)

import pandas as pd
import matplotlib.pyplot as plt

import sys

simulator_filename = sys.argv[1]
kyoto_filename = sys.argv[2]
osaka_filename = sys.argv[3]

# Read the 'c' column from each file
simulator_data = pd.read_csv(simulator_filename, header=None, usecols=[5])
kyoto_data = pd.read_csv(kyoto_filename, header=None, usecols=[5])
osaka_data = pd.read_csv(osaka_filename, header=None, usecols=[5])

# Plot the histograms
plt.hist(simulator_data[5], alpha=0.5, label='Simulator')
plt.hist(kyoto_data[5], alpha=0.5, label='FakeKyoto')
plt.hist(osaka_data[5], alpha=0.5, label='FakeOsaka')

# Set the title and labels
# plt.title('Distributions of C')
# plt.xlabel('c')
# plt.ylabel('Frequency')

# Show the legend
plt.legend(loc='upper right')

# Display the plot
# plt.show()
plt.savefig('histogram.png')
