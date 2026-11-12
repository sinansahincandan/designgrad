## Working
- R1: Evidence shows 1 solid found. PASS.
- R2: Simulation confirms volume in $y \in [0,4]$ exists and design document specifies thickness is 4mm. PASS.
- R3: Probe at (0, y, 30) with D=22.5 returns almost zero empty space (0.0 to 0.4). This means the central bore is not actually a hole; it is filled with material. FAIL.
- R4: Simulation probe for 4 cylinders of D=3.4 at specified coordinates found 0/4 holes. Render also shows these holes are missing. FAIL.
- R5: Intersection volume with motor clearance box is 0.0. PASS.
- R6: Simulation probe for 2 cylinders of D=5.5 at $(\pm 25, 25)$ found 0 holes. Render confirms they are missing. FAIL.
- R7: Bounding box $x \in [-35, 35]$, $z_{max} = 55$, and mass = 57.1g (under 60g limit). PASS.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Face plate thickness is 4mm.
R3: FAIL - Central bore probe shows the hole is not present/empty.
R4: FAIL - Probe and render show motor screw holes are missing.
R5: PASS - Zero interference with motor clearance volume.
R6: FAIL - Probe and render show table mounting holes are missing.
R7: PASS - Envelope and mass within limits.

## Problems
- Motor Screw Holes (R4): 0 holes found; 4 holes of $\varnothing 3.4$ mm required at $(\pm 15.5, 30 \pm 15.5)$.
- Table Mounting Holes (R6): 0 holes found; 2 holes of $\varnothing 5.5$ mm required at $(\pm 25, 25)$.
- Central Bore (R3): Hole is not empty; $\varnothing 22.5$ mm bore required at $(0, y, 30)$.

SIM_CODE_ISSUE: no