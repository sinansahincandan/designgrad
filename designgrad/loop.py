"""DesignGrad: textual-gradient optimisation of a design document d, CAD code c and simulation code s,
with persistent coding agents in the forward pass.

Levels (each adds one feedback channel; L1-L4 get the same number of design rounds K):
  L0 single prompt
  L1 TextGrad, overall-output critic only (code never executed)
  L2 + CAD execution feedback: the CAD agent repairs c until it builds one solid; measured geometry enters the loss
  L3 + agent-written simulation: the simulation agent writes s, runs it and repairs it until every requirement is
       measured; a reviewer checks each check simulates what the spec asks; only measured + faithful values enter the loss
  L4 + render feedback with a gate (mismatch -> c only; systemic -> d, restart from the design)
  L5 L2 + physics scenarios: instead of the measurement simulation, a test agent takes the built part into MuJoCo (physkit),
       writes realistic use scenarios (stand it on a desk, load it, tap it, push it), runs them and reports what happened;
       a reviewer checks each scenario is realistic; reviewed outcomes enter the loss and the score

Every candidate is critiqued once; its agent-visible score must strictly improve on the best so far to be kept.
"""
import json, re, shutil
from pathlib import Path

from . import prompts as P
from .agent import solve
from .llm import LLM, extract_code, extract_json
from .render import render
from .sandbox import run_cad, run_sim, report_feedback, phys_feedback, fmt_motion as _fmt_motion

LEVELS = ["L0", "L1", "L2", "L3", "L4", "L5"]


def _split_design(text: str):
    code = extract_code(text)
    i = text.find("```")
    d = (text[:i] if i >= 0 else text).strip()
    d = re.sub(r"^#+\s*Design document\s*", "", d, flags=re.I).strip()
    return d, code


def _improved(text: str, is_code: bool):
    m = re.search(r"<IMPROVED_VARIABLE>(.*?)(</IMPROVED_VARIABLE>|$)", text, flags=re.S)
    body = (m.group(1) if m else text).strip()
    return extract_code(body) if is_code else body


def _fmt_exec(m: dict) -> str:
    if not m.get("ok"):
        return "EXECUTION FAILED:\n" + str(m.get("error", "unknown error"))[-1500:]
    keep = {k: m[k] for k in ("n_solids", "valid", "bbox_min", "bbox_max", "size_mm", "volume_mm3", "mass_g",
                              "center_of_mass", "surface_area_mm2", "rest_stable", "rest_stability_margin_mm",
                              "n_cylindrical_faces") if k in m}
    keep["cylindrical_faces(first 16: radius, axis, centre)"] = m.get("cylindrical_faces", [])[:16]
    return "```json\n" + json.dumps(keep, indent=0) + "\n```"


def _critic_frac(loss: str, n_req: int, last: bool = False) -> float:
    """Fraction of requirements the critic marked PASS (UNSURE = 0.5), from lines like 'R3: FAIL - ...'.
    last=True (ladder v4): if a line revises itself ('FAIL - ... wait ... PASS'), its last verdict counts."""
    got = {}
    for line in loss.splitlines():
        mr = re.search(r"^\W*R(\d+)\b", line) if last else re.search(r"\bR(\d+)\b", line)
        vs = list(re.finditer(r"\b(PASS|FAIL|UNSURE)\b", line))
        mv = (vs[-1] if last else vs[0]) if vs else None
        if mr and mv and mr.start() < mv.start():
            got.setdefault(int(mr.group(1)), {"PASS": 1.0, "UNSURE": 0.5, "FAIL": 0.0}[mv.group(1)])
    return sum(got.get(i, 0.0) for i in range(1, n_req + 1)) / max(n_req, 1)


def _final_part(text: str):
    """v5 critic answer -> (verdicts + problems, verdicts only). Falls back to the whole text when the headings are missing."""
    mv = list(re.finditer(r"^\W*Verdicts\W*$", text, flags=re.I | re.M))
    if not mv:
        return text, text
    tail = text[mv[-1].start():]
    mp = re.search(r"^\W*Problems\b.*$", tail, flags=re.I | re.M)
    return tail.strip(), (tail[:mp.start()] if mp else tail)


def _measured(simr) -> dict:
    """Requirement -> entry, for checks that ran (pass/fail) and were not judged unfaithful."""
    if not simr or not simr.get("ok") or not isinstance(simr.get("result"), dict):
        return {}
    return {r: v for r, v in simr["result"].items() if v.get("status") in ("pass", "fail") and v.get("faithful") is not False}


def _sim_frac(simr):
    ms = _measured(simr)
    return sum(v["status"] == "pass" for v in ms.values()) / len(ms) if ms else 0.0


def _fmt_sim_evidence(simr, req_ids, disputed=False):
    ms = _measured(simr)
    lines_m, lines_u, lines_d = [], [], []
    rep = (simr or {}).get("result") or {}
    for r in req_ids:
        v = rep.get(r) if isinstance(rep, dict) else None
        if r in ms:
            lines_m.append(f"- {r}: {ms[r]['status'].upper()}  value={json.dumps(ms[r]['value'])[:80]}  method: {ms[r]['method'][:160]}  note: {ms[r]['note'][:120]}")
        elif v is None:
            lines_u.append(f"- {r}: no measurement" + ("" if simr and simr.get("ok") else " (simulation script did not run)"))
        elif disputed and v.get("faithful") is False and v.get("status") == "fail":
            lines_d.append(f"- {r}: FAIL  value={json.dumps(v.get('value'))[:80]}  method: {str(v.get('method', ''))[:160]}  reviewer: {v.get('why', '')[:200]}")
        elif v.get("faithful") is False:
            lines_u.append(f"- {r}: check judged not faithful to the specification ({v.get('why', '')[:140]})")
        else:
            lines_u.append(f"- {r}: check errored ({v.get('note', '')[:120]})")
    if disputed:
        return "\n".join(lines_m) or "(none)", "\n".join(lines_u) or "(none)", "\n".join(lines_d) or "(none)"
    return "\n".join(lines_m) or "(none)", "\n".join(lines_u) or "(none)"


def _fmt_phys_evidence(simr):
    ms = _measured(simr)
    lines_m, lines_u = [], []
    rep = (simr or {}).get("result") or {}
    if not (simr and simr.get("ok")):
        return "(none)", "- the scenario script did not run"
    for k, v in rep.items():
        reqs = ",".join(v.get("requirements") or [])
        if k in ms:
            lines_m.append(f"- {k} [{reqs}] {v['status'].upper()}: {v.get('scenario', '')[:220]}\n    observed: {v.get('observation', '')[:220]}"
                           + (f"\n    design feedback: {v.get('design_feedback', '')[:260]}" if v.get("design_feedback") else ""))
        elif v.get("faithful") is False:
            lines_u.append(f"- {k}: judged unrealistic ({v.get('why', '')[:140]})")
        else:
            lines_u.append(f"- {k}: errored ({v.get('note', '')[:120]})")
    return "\n".join(lines_m) or "(none)", "\n".join(lines_u) or "(none)"


class Run:
    def __init__(self, problem_dir: Path, level: str, out_root: Path, rounds: int = 4, repair_steps: int = 5, review_rounds: int = 3,
                 gate_fix: bool = False, ladder: str = "v2"):
        self.gate_fix = gate_fix   # L4 post-hoc render-review fix (measurement overrides render claims, no repeated failed restarts)
        # ladder "v4" (levels L0-L3): every level builds its code. L0 design + build, no feedback; L1 + critic that reads the design
        # document only; L2 + the agent's own analysis results; L3 + render review as one more piece of evidence (no restart rule).
        # ladder "v5": the same ladder with two general fixes. The critic writes its working first and then one final verdict per
        # requirement (only verdicts and problems go on to the gradient); the analysis script is also run on a control part (a 1 mm
        # cube) and the reviewer is told which checks pass on it; a design whose score cannot improve any more ends the loop.
        # ladder "v6": v5 plus fixes to the analysis channel (hole recipe in the reference sheet; control rule limited to checks that
        # pass on the control part; disputed FAIL measurements reach the critic as warnings; unverified requirements earn no credit).
        # ladder "v7": v6 plus a fix for false alarms of the analysis code (probes kept inside the feature, raw numbers reported,
        # the reviewer audits every failed check).
        self.v7 = ladder == "v7"
        self.v6 = ladder in ("v6", "v7")
        self.v5 = ladder in ("v5", "v6", "v7")
        self.v4 = ladder in ("v4", "v5", "v6", "v7")
        self.pd = Path(problem_dir)
        self.level = level
        self.phys = level == "L5"
        self.L = 2 if self.phys else LEVELS.index(level)   # L5 = L2 (CAD execution) + MuJoCo physics scenarios
        self.n = None
        if self.v4:
            self.n = int(level[1]); assert level in ("L0", "L1", "L2", "L3"), level
            self.L = {0: 2, 1: 2, 2: 3, 3: 4}[self.n]      # which machinery runs: build / + analysis agent / + render review
        self.K = rounds
        self.repair_steps = repair_steps
        self.review_rounds = review_rounds
        self.spec = (self.pd / "spec.md").read_text()
        self.req_ids = [f"R{i}" for i in range(1, max([int(x) for x in re.findall(r"\bR(\d+)\b", self.spec)] or [1]) + 1)]
        self.n_req = len(self.req_ids)
        self.meta = json.loads((self.pd / "meta.json").read_text())
        self.out = Path(out_root) / level / self.pd.name
        if self.out.exists():
            shutil.rmtree(self.out)
        self.out.mkdir(parents=True)
        self.llm = LLM(self.out / "calls.jsonl", cap=(1 if level == "L0" and not self.v4 else None))
        self.trace = []

    # ---------------------------------------------------------------- TextGrad backward + update
    def grad(self, role, value, loss, extra=""):
        return self.llm("gradient", P.GRAD_SYS, P.GRAD_USER.format(role=role, value=value, spec=self.spec, loss=loss, extra=extra))

    def update(self, role, value, g, is_code, context=""):
        txt = self.llm("update", P.UPD_SYS, P.UPD_USER.format(role=role, value=value, spec=self.spec, grad=g, context=context,
                                                             fmt=P.FMT_CODE if is_code else ""), max_tokens=6000)
        return _improved(txt, is_code)

    # ---------------------------------------------------------------- forward: persistent agents
    def build(self, k, d, c):
        """L2+: run c; if it fails or gives several solids, the CAD agent repairs it (conversation, <= repair_steps)."""
        rd = self.out / f"r{k:02d}"
        run = lambda code: run_cad(code, rd, self.meta["density"])

        def fb(m):
            if m.get("ok") and m.get("n_solids") == 1:
                return None
            if m.get("ok"):
                sol = m.get("solids", [])
                pieces = "\n".join(f"  solid {i + 1}: volume {x['volume_mm3']} mm3, bbox_min {x['bbox_min']}, bbox_max {x['bbox_max']}"
                                   for i, x in enumerate(sol))
                gaps = []
                for i, x in enumerate(sol[1:], start=2):  # where each piece sits relative to the largest one
                    b = sol[0]
                    sep = [(ax, max(x["bbox_min"][j] - b["bbox_max"][j], b["bbox_min"][j] - x["bbox_max"][j]), j)
                           for j, ax in enumerate("XYZ")]
                    far = [f"{s:.1f} mm along {ax} (solid 1 spans {ax.lower()} {b['bbox_min'][j]}..{b['bbox_max'][j]}, "
                           f"solid {i} spans {x['bbox_min'][j]}..{x['bbox_max'][j]})" for ax, s, j in sep if s > 0.01]
                    gaps.append(f"  solid {i} is separated from solid 1 by " + "; ".join(far) if far else
                                f"  solid {i}'s box touches or overlaps solid 1's box but the solids do not fuse: make them overlap by >= 1 mm")
                return (f"The code ran but produced {m.get('n_solids')} disconnected solids:\n{pieces}\n" + "\n".join(gaps) + "\n"
                        "`result` must be ONE connected solid. Compare these boxes: find which piece does not touch the main body, "
                        "extend or move it so it overlaps the body by at least 1 mm, and union everything into one solid.")
            return "The code failed:\n" + str(m.get("error", ""))[-1800:]

        a = solve(self.llm, "cad_agent", P.CAD_AGENT_SYS, P.CAD_AGENT_USER.format(d=d, c=c), run, fb,
                  max_steps=self.repair_steps, initial_code=c)
        return a["code"], a["result"], {"cad_steps": a["steps"], "cad_exhausted": a["exhausted"], "cad_history": a["history"]}

    def simulate(self, k, d, s_prev, m, critic_note=None):
        """L3+: the simulation agent writes/repairs s until every requirement is measured, then a reviewer checks
        each check is faithful to the specification; unfaithful checks go back to the agent (<= review_rounds)."""
        rd = self.out / f"r{k:02d}"
        info = {"sim_steps": 0, "sim_exhausted": False, "review": [], "sim_updated": False}
        if not m.get("ok"):
            return None, s_prev, info
        if self.phys:
            run = lambda code: run_sim(code, rd, timeout=300, phys=True, density=self.meta["density"])
            fb = phys_feedback
            SYS, task, role = P.PHYS_SYS, P.PHYS_USER.format(spec=self.spec, d=d, exec=_fmt_exec(m)), "phys_agent"
            REV_SYS, REV_USER, FIX_USER = P.PHYS_REVIEW_SYS, P.PHYS_REVIEW_USER, P.PHYS_FIX_USER
        else:
            run = lambda code: run_sim(code, rd)
            fb = lambda res: report_feedback(res, self.req_ids)
            SYS, task, role = (P.SIM_SYS_V6 if self.v6 else P.SIM_SYS), (P.SIM_USER_V7 if self.v7 else P.SIM_USER_V5 if self.v5 else P.SIM_USER).format(spec=self.spec, d=d), "sim_agent"
            REV_SYS, REV_USER, FIX_USER = P.SIM_REVIEW_SYS, (P.SIM_REVIEW_USER_V7 if self.v7 else P.SIM_REVIEW_USER), P.SIM_FIX_USER
        a = solve(self.llm, role, SYS, task, run, fb, max_steps=self.repair_steps + (3 if self.phys else 1), initial_code=s_prev,
                  max_tokens=9000 if self.phys else 6000, lenient=self.phys)
        s, simr = a["code"], a["result"]
        info.update({"sim_steps": a["steps"], "sim_exhausted": a["exhausted"], "sim_history": a["history"]})
        info["sim_updated"] = s_prev is None or s.strip() != s_prev.strip()
        findings = [critic_note] if critic_note else []
        for rr in range(self.review_rounds + 1):
            if simr.get("ok"):
                extra = {"motion": _fmt_motion(simr)} if self.phys else {}
                ctrl = self.control(k, s, m) if self.v5 and not self.phys else None
                ctrl_txt = ""
                if ctrl:
                    ok_ids = [r for r in self.req_ids if ctrl.get(r) == "pass"]
                    ctrl_txt = (P.SIM_REVIEW_CONTROL_V6 if self.v6 else P.SIM_REVIEW_CONTROL).format(passed=", ".join(ok_ids) or "(none)",
                                                           failed=", ".join(r for r in self.req_ids if r not in ok_ids) or "(none)")
                js = extract_json(self.llm(role.replace("agent", "reviewer"), REV_SYS, REV_USER.format(
                    spec=self.spec, exec=_fmt_exec(m), s=s, report=json.dumps(simr["result"], indent=0)[:6000], **extra) + ctrl_txt)) or {}
                bad = []
                for r in (list(simr["result"]) if self.phys else self.req_ids):
                    v = js.get(r)
                    if isinstance(v, dict) and v.get("faithful") is False and r in simr["result"]:
                        simr["result"][r]["faithful"] = False
                        simr["result"][r]["why"] = str(v.get("why", ""))[:300]
                        bad.append(f"{r}: {v.get('why', '')}")
                    elif r in simr["result"]:
                        simr["result"][r]["faithful"] = True
                info["review"].append({"round": rr, "unfaithful": [b.split(":")[0] for b in bad],
                                       **({"control_pass": [r for r in self.req_ids if ctrl.get(r) == "pass"]} if ctrl else {})})
                findings = findings + bad
            if not findings or rr == self.review_rounds:
                break
            # fix the criticised checks, then make sure the script still measures everything
            txt = self.llm(role, SYS, FIX_USER.format(findings="- " + "\n- ".join(findings), spec=self.spec, s=s),
                           max_tokens=6000, step=99)
            a = solve(self.llm, role, SYS, task, run, fb, max_steps=2, initial_code=extract_code(txt, self.phys), lenient=self.phys)
            s, simr = a["code"], a["result"]
            info["sim_steps"] += 1 + a["steps"]; info["sim_exhausted"] = a["exhausted"]; info["sim_updated"] = True
            findings = []
        simr = dict(simr or {}); simr["agent"] = {k2: info[k2] for k2 in ("sim_steps", "sim_exhausted", "review")}
        return simr, s, info

    def control(self, k, s, m):
        """v5: run the analysis script on a control part, a 1 mm cube at the part's lowest corner. Requirement -> status, or None."""
        try:
            cd = self.out / f"r{k:02d}" / "control"
            x0, y0, z0 = [float(v) for v in m["bbox_min"]]
            code = f'import cadquery as cq\nresult = cq.Workplane("XY").box(1, 1, 1, centered=False).translate(({x0}, {y0}, {z0}))\n'
            if not run_cad(code, cd, self.meta["density"]).get("ok"):
                return None
            r = run_sim(s, cd)
            if not r.get("ok") or not isinstance(r.get("result"), dict):
                return None
            return {rid: (v.get("status") if isinstance(v, dict) else None) for rid, v in r["result"].items()}
        except Exception:
            return None

    def max_score(self):
        return 1.0 + (1.0 if (self.L >= 3 or self.phys) else 0.0) + 1.0

    def forward(self, k, d, c, s_prev, critic_note=None):
        m, info, simr, s = {}, {}, None, s_prev
        if self.L >= 2:
            c, m, info = self.build(k, d, c)
        else:
            (self.out / f"r{k:02d}").mkdir(exist_ok=True)
        if self.L >= 3 or self.phys:
            simr, s, sinfo = self.simulate(k, d, s_prev, m, critic_note)
            info.update(sinfo)
        return {"k": k, "d": d, "c": c, "s": s, "m": m, "simr": simr, "info": info}

    # ---------------------------------------------------------------- loss
    def proxy(self, m, simr):
        """What the agent itself can see (never the hidden tests)."""
        if self.L < 2:
            return 0.0
        ran = 1.0 if (m.get("ok") and m.get("n_solids") == 1) else (0.5 if m.get("ok") else 0.0)
        if self.v6 and self.L >= 3:
            return ran + sum(v["status"] == "pass" for v in _measured(simr).values()) / self.n_req
        return ran + (_sim_frac(simr) if (self.L >= 3 or self.phys) else 0.0)

    def critique(self, cand):
        d, c, s, m, simr = cand["d"], cand["c"], cand["s"], cand["m"], cand["simr"]
        mism, systemic, gate = [], [], None
        if self.L >= 4 and m.get("ok"):
            rd = self.out / f"r{cand['k']:02d}"
            png = render(rd / "part.stl", rd / "views.png")
            js = extract_json(self.llm("image_critic", P.IMG_SYS, P.IMG_USER.format(spec=self.spec, d=d, exec=_fmt_exec(m)), images=[png])) or {}
            mism = [str(x) for x in js.get("mismatches", []) if x]
            for it in js.get("systemic", []) or []:
                if isinstance(it, dict) and it.get("issue"):
                    (systemic if it.get("render_faithful_here") else mism).append(str(it["issue"]))
            over = []
            if self.gate_fix:   # post-hoc ablation (runs/v2g_*), off for the main L4
                if m.get("n_solids", 1) != 1:  # several solids is a code problem: it goes to c, never a restart from the design
                    mism, systemic = mism + systemic, []
                # a measurement beats a picture: drop render claims whose requirements were all measured PASS (faithful checks)
                mp = {r for r, v in _measured(simr).items() if v["status"] == "pass"}
                names = lambda x: set(re.findall(r"\bR\d+\b", x))
                over = [x for x in mism + systemic if names(x) and names(x) <= mp]
                mism = [x for x in mism if x not in over]
                systemic = [x for x in systemic if x not in over]
            gate = {"mismatches": mism, "systemic": systemic, "summary": js.get("summary"),
                    **({"overridden_by_measurement": over} if self.gate_fix else {})}
        ev = ""
        if self.L >= 2 and not self.v4:
            ev += P.EVIDENCE_EXEC.format(exec=_fmt_exec(m))
        if self.L >= 3 and self.v6:
            meas, unm, disp = _fmt_sim_evidence(simr, self.req_ids, disputed=True)
            ev += P.EVIDENCE_SIM_V6.format(measured=meas, unmeasured=unm, disputed=disp)
        elif self.L >= 3:
            meas, unm = _fmt_sim_evidence(simr, self.req_ids)
            ev += P.EVIDENCE_SIM.format(measured=meas, unmeasured=unm)
        if self.phys:
            meas, unm = _fmt_phys_evidence(simr)
            ev += P.EVIDENCE_PHYS.format(measured=meas, unmeasured=unm, motion=_fmt_motion(simr))
        if gate:
            ev += (P.EVIDENCE_RENDER_FIX if self.gate_fix else P.EVIDENCE_RENDER).format(mism="\n".join("- " + x for x in mism) or "(none)",
                                           sysm="\n".join("- " + x for x in systemic) or "(none)")
        if self.v4 and not m.get("ok"):
            ev += "\n# Evidence: the code could not be built\n" + _fmt_exec(m) + "\n"
        if self.v4 and not ev:
            ev = P.EVIDENCE_NONE_V5 if self.v5 else P.EVIDENCE_NONE
        loss = self.llm("critic", P.CRITIC_SYS, (P.CRITIC_USER_V5 if self.v5 else P.CRITIC_USER_DOC if self.v4 else P.CRITIC_USER).format(
            spec=self.spec, d=d, c=c, evidence=ev, sim_question=P.SIM_LINE if self.L >= 3 else ""))
        full = None
        if self.v5:      # the working stays in critic_full.md; verdicts and problems are the loss that the gradient reads
            full, (loss, verdicts) = loss, _final_part(loss)
            cf = _critic_frac(verdicts, self.n_req, last=True)
        else:
            cf = _critic_frac(loss, self.n_req, last=self.v4)
        sim_issue = bool(self.L >= 3 and m.get("ok") and re.search(r"SIM_CODE_ISSUE:\s*yes", loss, re.I))
        return {"loss": loss, "gate": gate, "mism": mism, "systemic": systemic, "critic_frac": cf, "sim_issue": sim_issue,
                "score": self.proxy(m, simr) + cf, **({"loss_full": full} if full else {})}

    def save_round(self, k, **kw):
        rd = self.out / f"r{k:02d}"
        rd.mkdir(exist_ok=True)
        for name, val in kw.items():
            if val is None:
                continue
            (rd / name).write_text(val if isinstance(val, str) else json.dumps(val, indent=1, default=str))

    # ---------------------------------------------------------------- main
    def run(self):
        # All levels start from the SAME initial design: L0's single-prompt output, so levels differ only in the feedback they receive.
        l0 = self.out.parent.parent / "L0" / self.pd.name
        if self.level != "L0" and (l0 / "summary.json").exists():
            d, c = (l0 / "final_d.md").read_text(), (l0 / "final_c.py").read_text()
            self.llm.calls += 1
            with self.llm.log_path.open("a") as f:
                f.write(json.dumps({"i": 1, "role": "designer", "shared_from": "L0", "t": 0}) + "\n")
        else:
            txt = self.llm("designer", P.DESIGNER_SYS, P.DESIGNER_USER.format(spec=self.spec), max_tokens=6000)
            d, c = _split_design(txt)
        k = 0
        if self.L == 0:
            self.save_round(0, **{"d.md": d, "c.py": c})
            best = {"k": 0, "d": d, "c": c, "s": None, "score": 0.0}
        else:
            cand = self.forward(0, d, c, None)
            no_feedback = self.v4 and self.n == 0          # v4 L0: the first design, built; no critic, no rounds
            cr = ({"loss": "", "gate": None, "mism": [], "systemic": [], "critic_frac": 0.0, "sim_issue": False,
                   "score": self.proxy(cand["m"], None)} if no_feedback else self.critique(cand))
            best = {**cand, **cr}
            self._save(cand, cr)
            self.trace.append({"k": 0, "accepted": True, **self._rec(cand, cr)})
            note = ""
            for k in range(1, (0 if no_feedback else self.K) + 1):
                if self.v5 and best["score"] >= self.max_score() - 1e-9:   # every check and every verdict passes: no candidate can be kept
                    k -= 1
                    break
                d, c, s, loss = best["d"], best["c"], best["s"], best["loss"]
                mism, systemic = best["mism"], best["systemic"]
                rec = {"k": k, "from": best["k"]}
                if note:
                    loss = loss + "\n\n# Note from the optimizer\n" + note
                # ---- backward + update (gate: systemic -> d and restart from d; mismatch -> c)
                # do not repeat a restart from the same best design after the previous one was rejected
                failed_restart = bool(self.trace and self.trace[-1].get("restart_from_design") and not self.trace[-1]["accepted"]
                                      and self.trace[-1].get("from") == best["k"])
                restart = self.L >= 4 and len(systemic) > 0 and not self.v4 and not (self.gate_fix and failed_restart)
                extra_d = ("\nThe render review found these problems with the design itself (render faithful there):\n- " + "\n- ".join(systemic) + "\n") if systemic else ""
                extra_c = ("\nThe render review found these places where the built part does not match the design document:\n- " + "\n- ".join(mism) + "\n") if mism else ""
                gd = self.grad(P.ROLE_D, d, loss, extra_d)
                d_new = self.update(P.ROLE_D, d, gd, False)
                if restart:
                    c_new = extract_code(self.llm("designer_regen", P.DESIGNER_SYS, P.REGEN_C_USER.format(spec=self.spec, d=d_new), max_tokens=6000))
                    rec["restart_from_design"] = True
                else:
                    gc = self.grad(P.ROLE_C, c, loss, extra_c + f"\nThe design document is being updated to:\n<NEW_DESIGN_DOCUMENT>\n{d_new}\n</NEW_DESIGN_DOCUMENT>\n")
                    c_new = self.update(P.ROLE_C, c, gc, True, context=f"\nThe code must implement this (updated) design document:\n<DESIGN_DOCUMENT>\n{d_new}\n</DESIGN_DOCUMENT>\n")
                # ---- forward pass (agents repair until built / measured), then critique
                critic_note = ("The design critic flagged a measured simulation value as implausible:\n" + best["loss"][-1500:]) if best.get("sim_issue") else None
                cand = self.forward(k, d_new, c_new, s, critic_note)
                cr = self.critique(cand)
                self._save(cand, cr)
                accepted = cr["score"] > best["score"] + 1e-9
                rec.update({"accepted": accepted, **self._rec(cand, cr)})
                if accepted:
                    best = {**cand, **cr}
                    note = ""
                else:
                    note = (f"The last attempted update was rejected because it did not improve the agent-visible score "
                            f"({cr['score']:.2f} vs best {best['score']:.2f}). Its review said:\n{cr['loss'][-1200:]}")
                self.trace.append(rec)

        final = {"k": best["k"], "proxy": best["score"], "level": self.level, "problem": self.pd.name,
                 "llm": self.llm.stats(), "rounds": k, "trace": self.trace}
        (self.out / "final_d.md").write_text(best["d"])
        (self.out / "final_c.py").write_text(best["c"])
        if best.get("s"):
            (self.out / "final_s.py").write_text(best["s"])
        (self.out / "summary.json").write_text(json.dumps(final, indent=1, default=str))
        return final

    def _save(self, cand, cr):
        self.save_round(cand["k"], **{"d.md": cand["d"], "c.py": cand["c"], "s.py": cand["s"], "metrics.json": cand["m"] or None,
                                     "sim.json": cand["simr"], "loss.md": cr["loss"], "gate.json": cr["gate"], "agent.json": cand["info"] or None,
                                     "critic_full.md": cr.get("loss_full")})

    def _rec(self, cand, cr):
        info = cand["info"]
        ms = _measured(cand["simr"])
        return {"score": cr["score"], "proxy": cr["score"], "critic_frac": cr["critic_frac"], "gate": cr["gate"], "sim_issue": cr["sim_issue"],
                "cad_steps": info.get("cad_steps"), "cad_exhausted": info.get("cad_exhausted"),
                "sim_steps": info.get("sim_steps"), "sim_exhausted": info.get("sim_exhausted"), "sim_updated": info.get("sim_updated", False),
                "n_measured": len(ms) if (self.L >= 3 or self.phys) else None,
                "n_unmeasured": (len((cand["simr"] or {}).get("result") or {}) - len(ms) if self.phys else self.n_req - len(ms)) if (self.L >= 3 or self.phys) else None,
                "review": info.get("review")}
