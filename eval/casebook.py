"""Casebook: feedback -> design change -> hidden-test outcome, with renders, for the paper.

python eval/casebook.py runs/v2_all [runs/l6mj ...]     -> paper/casebook/index.md + one page per case + images

A case is one update the loop made (round k, started from the best round f): which requirements it newly passed or broke in the
hidden tests, the feedback it acted on (critic lines, simulation / scenario / render evidence about those requirements in round f),
and the parts before and after. Also writes a level-comparison page per problem unit (final design of every level).
Needs hidden_rows.json in round folders (eval/mechanics.py writes them)."""
import json, re, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "paper" / "figs"))
OUT = ROOT / "paper" / "casebook"
IMG = OUT / "img"
FONT = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 22)


def render(stl: Path, png: Path):
    if not png.exists() and stl.exists():
        from vtk_render import render as vr
        vr(stl, png, 520)
    return png if png.exists() else None


def tile(png, label, sub, color=(29, 36, 51)):
    im = Image.new("RGB", (520, 600), "white")
    if png:
        p = Image.open(png).convert("RGBA"); bg = Image.new("RGBA", p.size, (246, 247, 249, 255)); bg.alpha_composite(p)
        im.paste(bg.convert("RGB").resize((520, 520)), (0, 0))
    else:
        ImageDraw.Draw(im).text((180, 250), "did not build", fill=(120, 120, 120), font=FONT)
    d = ImageDraw.Draw(im)
    d.text((14, 530), label, fill=(29, 36, 51), font=FONT); d.text((14, 562), sub, fill=color, font=FONT)
    return im


def hidden(rd):
    p = rd / "hidden_rows.json"
    return json.loads(p.read_text()) if p.exists() else None


def lines_about(text, rids):
    out = []
    for ln in (text or "").splitlines():
        if any(re.search(rf"\b{r}\b", ln) for r in rids) and len(ln.strip()) > 8:
            out.append(ln.strip()[:400])
    return out[:6]


def evidence(rd, rids):
    ev = []
    try:
        sim = json.loads((rd / "sim.json").read_text()).get("result") or {}
    except Exception:
        sim = {}
    for k, v in sim.items():
        if not isinstance(v, dict):
            continue
        reqs = v.get("requirements") or ([k] if k.startswith("R") else [])
        if any(r in reqs for r in rids):
            ev.append(f"[{'scenario' if k.startswith('S') else 'simulation'} {k}: {v.get('status')}] "
                      + (v.get("scenario") or v.get("method") or "")[:200]
                      + (f" | observed: {v.get('observation')[:200]}" if v.get("observation") else "")
                      + (f" | value: {json.dumps(v.get('value'))[:120]}" if v.get("value") is not None and not v.get("observation") else "")
                      + (f" | design feedback: {v.get('design_feedback')[:250]}" if v.get("design_feedback") else ""))
    try:
        g = json.loads((rd / "gate.json").read_text()) or {}
        for x in (g.get("mismatches") or []) + (g.get("systemic") or []):
            if any(re.search(rf"\b{r}\b", x) for r in rids):
                ev.append(f"[render gate] {x[:300]}")
    except Exception:
        pass
    return ev[:6]


def run_cases(run_root: Path):
    cases = []
    for summ in sorted(run_root.glob("L*/*/summary.json")):
        unit = summ.parent; level = unit.parent.name
        S = json.loads(summ.read_text())
        H = {t["k"]: hidden(unit / f"r{t['k']:02d}") for t in S["trace"]}
        for t in S["trace"][1:]:
            f, k = t.get("from"), t["k"]
            if f is None or H.get(f) is None or H.get(k) is None:
                continue
            gained = [r for r in H[k] if H[k][r] is True and H[f].get(r) is False]
            lost = [r for r in H[k] if H[k][r] is False and H[f].get(r) is True]
            if not gained and not lost:
                continue
            rd_f = unit / f"r{f:02d}"
            loss = (rd_f / "loss.md").read_text() if (rd_f / "loss.md").exists() else ""
            cases.append({"run": run_root.name, "level": level, "unit": unit.name, "from": f, "k": k, "accepted": t["accepted"],
                          "gained": gained, "lost": lost, "critic": lines_about(loss, gained + lost), "evidence": evidence(rd_f, gained + lost),
                          "h_from": sum(v is True for v in H[f].values()), "h_k": sum(v is True for v in H[k].values()), "n": len(H[k]),
                          "dir_f": rd_f, "dir_k": unit / f"r{k:02d}", "restart": t.get("restart_from_design", False)})
    return cases


def write_case(c, i):
    name = f"{c['run']}_{c['level']}_{c['unit'].replace('@', '_')}_r{c['k']}"
    a = render(c["dir_f"] / "part.stl", IMG / f"{name}_before.png")
    b = render(c["dir_k"] / "part.stl", IMG / f"{name}_after.png")
    good = (0, 140, 90); bad = (200, 50, 50)
    t1 = tile(a, f"round {c['from']} (held as best)", f"hidden {c['h_from']}/{c['n']}")
    t2 = tile(b, f"round {c['k']} ({'kept' if c['accepted'] else 'rejected'})", f"hidden {c['h_k']}/{c['n']}  "
              + (f"+{','.join(c['gained'])} " if c["gained"] else "") + (f"-{','.join(c['lost'])}" if c["lost"] else ""),
              good if c["h_k"] > c["h_from"] else bad)
    pair = Image.new("RGB", (1060, 600), "white"); pair.paste(t1, (0, 0)); pair.paste(t2, (540, 0))
    pair.save(IMG / f"{name}.png")
    md = [f"# {c['level']} · {c['unit']} · round {c['from']} → {c['k']}", "",
          f"![]({'img/' + name + '.png'})", "",
          f"**Hidden tests:** {c['h_from']}/{c['n']} → {c['h_k']}/{c['n']}"
          + (f"; newly passed {', '.join(c['gained'])}" if c["gained"] else "") + (f"; newly failed {', '.join(c['lost'])}" if c["lost"] else "")
          + f"; update {'kept' if c['accepted'] else 'rejected'} by keep-best" + ("; restart from the design" if c["restart"] else ""), "",
          "**Feedback the update acted on (critic, round %d):**" % c["from"], ""] + [f"> {x}" for x in c["critic"] or ["(no line names these requirements)"]] + \
         ["", "**Evidence behind it:**", ""] + [f"- {x}" for x in c["evidence"] or ["(critic only)"]]
    (OUT / f"{name}.md").write_text("\n".join(md) + "\n")
    return name


def level_pages(run_root: Path):
    pages = []
    units = sorted({p.name for p in run_root.glob("L*/*") if (p / "summary.json").exists()})
    for u in units:
        tiles = []
        for lv in sorted(p.name for p in run_root.glob("L*") if (p / u / "summary.json").exists()):
            ud = run_root / lv / u
            S = json.loads((ud / "summary.json").read_text())
            H = hidden(ud / f"r{S['k']:02d}") if lv != "L0" else hidden(ud / "r00")
            stl = ud / "eval_final" / "part.stl"
            if not stl.exists():
                stl = ud / f"r{S['k']:02d}" / "part.stl"
            png = render(stl, IMG / f"{run_root.name}_{u.replace('@', '_')}_{lv}_final.png")
            n = sum(v is True for v in H.values()) if H else 0
            tiles.append(tile(png, lv, f"hidden {n}/{len(H) if H else '?'}"))
        if not tiles:
            continue
        row = Image.new("RGB", (540 * len(tiles), 600), "white")
        for i, t in enumerate(tiles):
            row.paste(t, (540 * i, 0))
        name = f"levels_{run_root.name}_{u.replace('@', '_')}"
        row.save(IMG / f"{name}.png")
        pages.append(name)
    return pages


def main(roots):
    IMG.mkdir(parents=True, exist_ok=True)
    allc, pages = [], []
    for r in roots:
        allc += run_cases(Path(r))
        pages += level_pages(Path(r))
    allc.sort(key=lambda c: (-(len(c["gained"]) - len(c["lost"])) * (1 if c["accepted"] else 0.5), c["level"]))
    idx = ["# Casebook: feedback → design change → hidden-test outcome", "",
           "Each case is one update of the loop. Ranked by hidden-test gain of kept updates; regressions and rejected updates follow.", "",
           "| case | level | unit | round | hidden | kept | gained | lost | evidence type |", "|---|---|---|---|---|---|---|---|---|"]
    for i, c in enumerate(allc):
        name = write_case(c, i)
        et = sorted({e.split(']')[0].strip('[').split(' ')[0] for e in c["evidence"]}) or ["critic"]
        idx.append(f"| [{i + 1}]({name}.md) | {c['level']} | {c['unit']} | {c['from']}→{c['k']} | {c['h_from']}→{c['h_k']}/{c['n']} | "
                   f"{'yes' if c['accepted'] else 'no'} | {','.join(c['gained'])} | {','.join(c['lost'])} | {', '.join(et)} |")
    idx += ["", "## Same problem, every level (final designs)", ""] + [f"![]({'img/' + p + '.png'})" for p in pages]
    (OUT / "index.md").write_text("\n".join(idx) + "\n")
    print(f"{len(allc)} cases, {len(pages)} level pages -> {OUT / 'index.md'}")


if __name__ == "__main__":
    main(sys.argv[1:])
