#!/usr/bin/env bash
# John Hurst, 2024-03-30

SCRIPTDIR=$(cd $(dirname $0); pwd)
SCRIPTNAME=$(basename $0)
PYSCRIPT="${SCRIPTDIR}/${SCRIPTNAME%.*}.py"

for STATE in phiplus phiminus psiplus psiminus; do
  $PYSCRIPT --$STATE --filename="images/qiskit_${STATE}.png"
done

for TARGET in heron eagle falcon; do
  for STATE in phiplus phiminus psiplus psiminus; do
    $PYSCRIPT --$STATE --transpile=$TARGET --filename="images/qiskit_${STATE}_${TARGET}.png"
  done
done
