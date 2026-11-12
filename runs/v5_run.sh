#!/bin/zsh
# The paper's ladder (v5: L0-L3, every level builds; critic and analysis fixes): 3 test problems x 3 seeds. Resumable.
cd "$(dirname "$0")/.."
for s in 0 1000 2000; do
  echo "=== v5 seed $s $(date)"
  DG_SEED=$s .venv/bin/python -m designgrad.run --ladder v5 --problems P01 P03 P07 --levels L0 L1 L2 L3 --out runs/v5_s$s
done
echo "=== ALL DONE $(date)"
