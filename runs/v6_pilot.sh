#!/bin/zsh
# Pilot of the ladder with the analysis-channel fixes (v6) on a development problem (L0 copied from runs/v5pilot: same code path).
cd "$(dirname "$0")/.."
echo "=== v6 pilot $(date)"
DG_SEED=0 .venv/bin/python -m designgrad.run --ladder v6 --problems ${1:-P08} --levels L0 L2 L3 --out runs/v6pilot
echo "=== ALL DONE $(date)"
