#!/usr/bin/env bash
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-05-19

SCRIPTDIR=$(cd $(dirname $0); pwd)
PY="$SCRIPTDIR/homework3_q1_qiskit.py"

PROVIDER=$1
THETA=$2

$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi=0
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="pi/12"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="pi/6"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="pi/4"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="pi/3"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="5*pi/12"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="pi/2"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="7*pi/12"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="2*pi/3"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="3*pi/4"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="5*pi/6"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="11*pi/12"
$PY --realign --proportion --provider=$PROVIDER --theta=$THETA --phi="pi"
