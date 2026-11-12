#!/bin/zsh
# Pilot of the paper's ladder (v4: L0-L3, every level builds) on a development problem.
cd "$(dirname "$0")/.."
echo "=== v4 pilot $(date)"
DG_SEED=0 .venv/bin/python -m designgrad.run --ladder v4 --problems ${1:-P08} --levels L0 L1 L2 L3 --out runs/v4pilot
echo "=== ALL DONE $(date)"
