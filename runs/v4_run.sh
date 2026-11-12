#!/bin/zsh
# The paper's ladder (v4: L0-L3, every level builds): 3 test problems x 3 seeds. Resumable: finished units are skipped.
cd "$(dirname "$0")/.."
for s in 0 1000 2000; do
  echo "=== v4 seed $s $(date)"
  DG_SEED=$s .venv/bin/python -m designgrad.run --ladder v4 --problems P01 P03 P07 --levels L0 L1 L2 L3 --out runs/v4_s$s
done
echo "=== ALL DONE $(date)"
