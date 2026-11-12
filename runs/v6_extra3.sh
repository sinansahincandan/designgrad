#!/bin/zsh
# Second repeat (seed 1000) of the pipe clamp, drone arm and heat sink, resumed after the pause. Finished units are skipped.
cd "$(dirname "$0")/.."
for p in P05 P09 P06; do
  if [ $(date +%d%H%M) -ge 121345 ]; then echo "=== time guard: skip $p seed 1000 $(date)"; continue; fi
  echo "=== v6 extra $p seed 1000 $(date)"
  DG_SEED=1000 .venv/bin/python -m designgrad.run --ladder v6 --problems $p --levels L0 L1 L2 L3 --out runs/v6x_s1000
done
echo "=== EXTRA3 DONE $(date)"
