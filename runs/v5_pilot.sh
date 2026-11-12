#!/bin/zsh
# Pilot of the ladder with the critic and analysis fixes (v5) on a development problem.
cd "$(dirname "$0")/.."
echo "=== v5 pilot $(date)"
DG_SEED=0 .venv/bin/python -m designgrad.run --ladder v5 --problems ${1:-P08} --levels L0 L1 L2 L3 --out runs/v5pilot
echo "=== ALL DONE $(date)"
