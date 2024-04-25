#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

parser = argparse.ArgumentParser(description='Plot histograms of C values from CSV files.')
parser.add_argument('--filename', type=str, help='Filename for histogram')
parser.add_argument('--size', type=str, help='Size of histogram')
parser.add_argument('files', metavar='file', type=str, nargs='+', help='CSV files to plot')
args = parser.parse_args()

plt.figure(figsize=(20, 6))
for filename in args.files:
    data = pd.read_csv(filename, header=None, usecols=[5])
    plt.hist(data[5], alpha=0.5, label=filename.replace('.csv', ''))

# Set the size of the plot
# Set the title and labels
# plt.title('Distributions of C')
# plt.xlabel('c')
# plt.ylabel('Frequency')

# Show the legend
plt.legend(loc='upper right')

if args.filename:
    plt.savefig(args.filename)
else:
    plt.show()
