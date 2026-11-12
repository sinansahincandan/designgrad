"""Example figures of the paper (ladder v4): the same first design, read by the three critics.   python paper/figs/v4_examples.py
One row per level: part before -> what the critic read and said -> the change in the design document -> part after (requirements met
by the independent tests on the badge). Every quote is copied from the recorded run (critic: r{parent}/loss.md, design document: d.md);
"..." marks an omission."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_figs_v4 as F

RUN = "runs/v6_s0"

MOTOR = [
    dict(level="L1", k=1, head="the design document",
         reads=["Only the text. It finds a dimension the document never states."],
         critic=["R5: UNSURE - Pocket dimensions for motor clearance are not provided.",
                 "Missing Pocket Dimensions: The motor clearance pocket dimensions are not specified (R5)."],
         diff=[("-", "Motor Interface: A recessed area to accommodate the NEMA 17 body while maintaining screw alignment."),
               ("+", "Motor Clearance Pocket: A rectangular subtraction defined by the volume x in [-21.5, 21.5], y in [0, 4], and z in [8.5, 51.5].")]),
    dict(level="L2", k=1, head="+ its own analysis",
         reads=["Its analysis code probed the built part: no bore, no screw holes, no material around them."],
         critic=["R3: FAIL - Cylinder probe at (0, y, 30) found no bore or walls.",
                 "Face Plate Integrity: The face plate is not a solid 4mm thick slab (R2); volume ratio is only 0.189."],
         diff=[("-", "Face Plate: Located at y in [0, 4], containing the motor mounting holes and central bore."),
               ("+", "Face Plate: A solid rectangular block defined by x in [-35, 35], y in [0, 4], and z in [0, 55].")]),
    dict(level="L3", k=1, head="+ four views", views=True,
         reads=["The same measurements, and four rendered views."],
         critic=["Orientation: Face plate is oriented in the XZ plane extending into negative Z; should be y in [0, 4].",
                 "Base Plate Location: Located in negative Z region; should be at z >= 0."],
         diff=[("-", "Base Plate: Located at z in [0, 5], providing the mounting surface for the table."),
               ("+", "Base Plate: A horizontal plate resting on the table (z=0), extending upwards in the +Z direction to provide a mounting surface.")]),
]


BRACKET = [   # second repeat... numbers at work: runs/v6_s2000, L2
    dict(level="L2", k=1, head="+ its own analysis",
         reads=["Its analysis code measured the built part: 444.8 g, and too wide on one side."],
         critic=["Mass: Current mass is 444.84 g; must be <= 90 g.",
                 "Y-Envelope: Current y-range is [-10, 40]; must be within [-20, 20]."],
         diff=[("-", "Profile at x=10: A deep rectangular section (approx. height 90mm, width 40mm) to satisfy strength and stiffness requirements."),
               ("+", "Profile at x=10: A hollow rectangular section (approx. height 90mm, width 40mm) to satisfy R5 (strength) and R6 (stiffness) while drastically reducing volume ...")]),
    dict(level="L2", k=2, head="+ its own analysis",
         reads=["One round later the same code measures 42.9 g. Two items are left."],
         critic=["R7: PASS - mass = 42.85 g <= 90 g.",
                 "Screw Clearance (R3): The clearance volume for x >= 10 is 0; it must be non-zero to allow screwdriver access."],
         diff=[("-", "... clearance channels (radius >= 4mm) cut for all x >= 10 to ensure screwdriver access."),
               ("+", "... clearance channels (radius >= 4mm) cut via boolean subtraction for all x >= 10 to ensure screwdriver access.")]),
]

MOTOR2 = [    # runs/v6_s1000, L3: two rounds, two steps
    dict(level="L3", k=1, head="+ four views", views=True,
         reads=["Measurements and four views of the first design."],
         critic=["Motor Clearance: Intersection volume 6910.28 mm^3 (should be 0)."],
         diff=[("-", "Motor Interface: The face plate is recessed/cut to ensure motor clearance."),
               ("+", "Motor Clearance (R5): To ensure zero interference with the motor body, a large void is maintained in the region defined by x in [-21.5, 21.5], y in [-48, 0], and z in [8.5, 51.5].")]),
    dict(level="L3", k=2, head="+ four views", views=True,
         reads=["The clearance is now free. The holes are next."],
         critic=["Central Bore (R3): Diameter is 0.4 mm; should be 22.5 mm."],
         diff=[("-", "R3 (Central Bore): A dia. 22.5 mm hole is drilled through the face plate along the Y-axis, centered at (x=0, z=30)."),
               ("+", "R3 (Central Bore): A dia. 22.5 mm hole (implemented as a subtractive cylinder with radius 11.25 mm) is drilled through the face plate along the Y-axis, centered at (x=0, z=30).")]),
]


def check(problem, rows, run=None):
    """Every quote must be found in the records (after plain())."""
    import json, re
    sq = lambda s: re.sub(r"\s+", " ", F.plain(s)).strip()
    for row in rows:
        rd = F.ROOT / (run or RUN) / row["level"] / problem
        t = {x["k"]: x for x in json.loads((rd / "summary.json").read_text())["trace"]}[row["k"]]
        loss = sq((rd / f"r{t['from']:02d}/loss.md").read_text())
        docs = {"-": sq((rd / f"r{t['from']:02d}/d.md").read_text()), "+": sq((rd / f"r{row['k']:02d}/d.md").read_text())}
        for q in row["critic"]:
            for part in [p.strip() for p in q.split("...") if p.strip()]:
                assert sq(part) in loss, (row["level"], row["k"], "critic", part)
        for sign, q in row["diff"]:
            for part in [p.strip() for p in q.split("...") if p.strip()]:
                assert sq(part) in docs[sign], (row["level"], row["k"], sign, part)
    print("quotes verified:", problem)


if __name__ == "__main__":
    check("P07_nema17_mount", MOTOR)
    F.example(RUN, "P07_nema17_mount", MOTOR, "v6_ex_motor", title="Motor mount: the same first design, read by three critics")
    check("P01_shelf_bracket", BRACKET, "runs/v6_s2000")
    F.example("runs/v6_s2000", "P01_shelf_bracket", BRACKET, "v6_ex_bracket", title="Shelf bracket, L2: two rounds driven by the agent's own measurements")
    check("P07_nema17_mount", MOTOR2, "runs/v6_s1000")
    F.example("runs/v6_s1000", "P07_nema17_mount", MOTOR2, "v6_ex_motor2", title="Motor mount, L3 (another repeat): one fault at a time")
