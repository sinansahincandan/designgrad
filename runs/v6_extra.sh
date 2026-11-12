#!/bin/zsh
# Five further parts with the paper's ladder (v6), queued behind the main run: one repeat each (seed 0), then a second repeat
# (seed 1000) for as many as fit before 11:30. Resumable: finished units are skipped.
cd "$(dirname "$0")/.."
until grep -q "ALL DONE" runs/v6_run.log; do sleep 30; done
for s in 0 1000; do
  for p in P02 P10 P05 P09 P06; do
    if [ $s != 0 ] && [ $(date +%d%H%M) -ge 121130 ]; then echo "=== time guard: skip $p seed $s $(date)"; continue; fi
    echo "=== v6 extra $p seed $s $(date)"
    DG_SEED=$s .venv/bin/python -m designgrad.run --ladder v6 --problems $p --levels L0 L1 L2 L3 --out runs/v6x_s$s
  done
  echo "=== EXTRA SEED $s DONE $(date)"
done
echo "=== ALL DONE $(date)"
