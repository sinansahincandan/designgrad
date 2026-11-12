#!/bin/zsh
# The paper's ladder (v7: L0-L3, every level builds; critic, analysis-channel and false-alarm fixes): 3 test problems x 3 seeds. Resumable.
# L0 and L1 are not affected by the v6/v7 fixes (replay identical): seed 0 L0+L1 and seed 1000 L0/P01 are copied from the v5/v6 runs.
cd "$(dirname "$0")/.."
for s in 0 1000 2000; do
  echo "=== v7 seed $s $(date)"
  DG_SEED=$s .venv/bin/python -m designgrad.run --ladder v7 --problems P01 P03 P07 --levels L0 L1 L2 L3 --out runs/v7_s$s
done
echo "=== ALL DONE $(date)"
