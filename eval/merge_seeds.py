"""Merge seed replicates into one analysis folder via symlinks, so every eval script sees problem-seed units.

python eval/merge_seeds.py runs/v2_all runs/v2_s0 runs/v2_s1000 runs/v2_s2000
-> runs/v2_all/L*/P01_shelf_bracket@s0 -> ../../v2_s0/L*/P01_shelf_bracket  (etc.)
Then: eval/evaluate_runs.py runs/v2_all; eval/analyze.py runs/v2_all test; eval/mechanics.py ...; eval/blind_pack.py ...
"""
import os, re, shutil, sys
from pathlib import Path


def main(dst: Path, srcs: list[Path]):
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    n = 0
    for src in srcs:
        m = re.search(r"s(\d+)$", src.name)
        tag = f"s{m.group(1)}" if m else src.name
        for lv in sorted(p for p in src.glob("L*") if p.is_dir()):
            for rd in sorted(p for p in lv.glob("P*") if p.is_dir() and (p / "summary.json").exists()):
                d = dst / lv.name
                d.mkdir(exist_ok=True)
                os.symlink(os.path.relpath(rd.resolve(), d.resolve()), d / f"{rd.name}@{tag}")
                n += 1
    print(f"{n} runs linked into {dst}")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), [Path(s).resolve() for s in sys.argv[2:]])
