# Entry points

There is no training step: the agents are an off-the-shelf model (Gemma 4 26B-A4B via Ollama) driven by prompts. "Prediction" is
running the design loop on a problem; evaluation is running the frozen independent tests on its outputs.

## The paper's ladder (v6)

`--ladder v6` selects the ladder reported in `paper/DesignGrad_v4.pdf`: L0 design and build, no feedback; L1 + a critic that reads the
design document; L2 + the agent's own analysis (tested on a control part); L3 + render review.

1. `ollama pull gemma4:26b` — the model (Apache-2.0).
2. `.venv/bin/python eval/validate_refs.py` — every reference design passes its independent tests; plain blocks fail.
3. `.venv/bin/python eval/freeze.py --check FROZEN_v7.json` — specifications, independent tests and loop code against the manifest.
4. `DG_SEED=<seed> .venv/bin/python -m designgrad.run --ladder v6 --problems <P..> --levels L0 L1 L2 L3 --out runs/<name>` — runs the
   agents; writes every round to `runs/<name>/<level>/<problem>/rNN/`.
5. `.venv/bin/python eval/v4_analyze.py runs/<name> [more runs] --out runs/<out>` — independent tests on every round; tables in
   `v4_summary.md`, numbers in `v4_summary.json`.
6. `DG_LADDER=v6 .venv/bin/python eval/replay.py runs/<name> <level> <problem>` — record-replay check of one run.
7. `.venv/bin/python paper/figs/make_figs_v6.py`, `paper/figs/make_figs_v4.py loop`, `paper/figs/v4_examples.py` — figures (quotes are
   verified against the records). `make_figs_v6.py casebook` lists every kept round that met more requirements than its parent.
8. `.venv/bin/python paper/build_pdf.py draft_v4.md DesignGrad_v4` — the PDF (needs a local Chrome).

## Reported runs

1. `runs/v6_run.sh` — three parts x three seeds -> `runs/v6_s0`, `runs/v6_s1000`, `runs/v6_s2000`, scored in `runs/v6_all`. Seed 0
   started from the state in `FROZEN_v6.json`; the remaining seeds ran with the state in `FROZEN_v7.json`, flag `--ladder v6`.
2. `runs/v6_extra.sh` — five further parts, one repeat -> `runs/v6x_s0`. `runs/v6_extra2.sh`, `runs/v6_extra3.sh` — second repeat of
   four of them -> `runs/v6x_s1000`; both scored in `runs/v6x_all`. Left out of Fig. 10 and named in Section 4.5: the tilted sensor
   mount (P10; CAD code out of steps in 12 of 16 builds) and the pipe clamp's second repeat (10 of 16).
3. Logs: `runs/v6_run.log`, `runs/v6_extra.log`; replay checks: `runs/_replay_v*_check*.log`.

## Earlier versions of the loop

`runs/v4_s0` and `runs/v5_s0` are first passes with `--ladder v4` and `--ladder v5`; the faults they showed led to the revisions
listed in the paper's Limitations. `runs/v7_s0` (`--ladder v7`, a reviewer that audits every failed check) lowered false alarms but
let the checks miss real faults; by a rule stated before the comparison it was not adopted. `--ladder v2` and the scripts
`eval/evaluate_runs.py`, `analyze.py`, `mechanics.py`, `loopcheck.py`, `blind_pack.py`, `judge_summary.py`, `casebook.py`,
`merge_seeds.py`, `l5_*.py` belong to earlier ladders whose records are not in this repository.
