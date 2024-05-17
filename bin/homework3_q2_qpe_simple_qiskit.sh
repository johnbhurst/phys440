#!/usr/bin/env bash
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-05-18

SCRIPTDIR=$(cd $(dirname $0); pwd)
BASHNAME=$(basename $0)
PY=$(echo "$SCRIPTDIR/$BASHNAME" | sed 's/\.sh/.py/')

# With manual QFT implementation:
$PY --operator=Z --eigenvector=e0 --filename=homework2_q2_qpe_z_e0.png --isa-filename=homework2_q2_qpe_z_e0_isa.png
$PY --operator=Z --eigenvector=e1 --filename=homework2_q2_qpe_z_e1.png --isa-filename=homework2_q2_qpe_z_e1_isa.png
$PY --operator=Y --eigenvector=e0 --filename=homework2_q2_qpe_y_e0.png --isa-filename=homework2_q2_qpe_y_e0_isa.png
$PY --operator=Y --eigenvector=e1 --filename=homework2_q2_qpe_y_e1.png --isa-filename=homework2_q2_qpe_y_e1_isa.png

# With builtin QFT implementation:
$PY --operator=Z --eigenvector=e0 --qft --filename=homework2_q2_qpe_z_e0_qft.png --isa-filename=homework2_q2_qpe_z_e0_qft_isa.png
$PY --operator=Z --eigenvector=e1 --qft --filename=homework2_q2_qpe_z_e1_qft.png --isa-filename=homework2_q2_qpe_z_e1_qft_isa.png
$PY --operator=Y --eigenvector=e0 --qft --filename=homework2_q2_qpe_y_e0_qft.png --isa-filename=homework2_q2_qpe_y_e0_qft_isa.png
$PY --operator=Y --eigenvector=e1 --qft --filename=homework2_q2_qpe_y_e1_qft.png --isa-filename=homework2_q2_qpe_y_e1_qft_isa.png