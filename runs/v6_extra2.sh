#!/bin/zsh
# Second repeat (seed 1000) of the further parts shown in the paper. Replaces the tail of runs/v6_extra.sh: the tilted sensor mount
# (P10) is left out of the paper (its CAD code ran out of steps in 12 of 16 builds), so its second repeat is skipped.
# Waits for the phone stand's second repeat, already running, then runs the other three. Resumable.
cd "$(dirname "$0")/.."
while kill -0 $1 2>/dev/null; do sleep 20; done
echo "=== extra2: P02 seed 1000 finished $(date)"
for p in P05 P09 P06; do
  if [ $(date +%d%H%M) -ge 121315 ]; then echo "=== time guard: skip $p seed 1000 $(date)"; continue; fi
  echo "=== v6 extra $p seed 1000 $(date)"
  DG_SEED=1000 .venv/bin/python -m designgrad.run --ladder v6 --problems $p --levels L0 L1 L2 L3 --out runs/v6x_s1000
done
echo "=== EXTRA2 DONE $(date)"
