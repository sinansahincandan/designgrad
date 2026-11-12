#!/bin/zsh
# The paper's ladder (v6: L0-L3, every level builds; critic and analysis-channel fixes): 3 test problems x 3 seeds. Resumable.
# L0 and L1 of seed 0 are copied from runs/v5_s0 (v6 changes only the analysis channel; replay of those units under v6 is identical).
cd "$(dirname "$0")/.."
for s in 0 1000 2000; do
  echo "=== v6 seed $s $(date)"
  DG_SEED=$s .venv/bin/python -m designgrad.run --ladder v6 --problems P01 P03 P07 --levels L0 L1 L2 L3 --out runs/v6_s$s
done
echo "=== ALL DONE $(date)"
