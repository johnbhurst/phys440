#!/usr/bin/env python
# John Hurst (john.b.hurst@gmail.com)
# 2024-05-25

import argparse
import pandas as pd
import sys


parser = argparse.ArgumentParser(description='Combine CSV files into a single DataFrame.')
parser.add_argument('files', metavar='file', type=str, nargs='+', help='a CSV file to combine')
args = parser.parse_args()

# Initialize an empty DataFrame to hold the combined data
combined_data = pd.DataFrame()

# Loop through the list of CSV file names
for csv_file in args.files:
    # Read the data into a DataFrame
    data = pd.read_csv(csv_file, header=None)

    # Rename the column to the file name without the ".csv" extension
    data.columns = [csv_file.replace('.csv', '')]

    # Join this DataFrame with the combined data DataFrame
    combined_data = pd.concat([combined_data, data], axis=1)

# Print the combined data DataFrame to the console
# print(combined_data)
combined_data.to_csv(sys.stdout, index=False)
