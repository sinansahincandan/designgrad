## Working
- R1: PASS. The design document and simulation confirm one single solid.
- R2: PASS. BBox shows 40x40 mm footprint and 23 mm height (<= 25 mm).
- R3: PASS. Intersection volume in z=[0,3] is ~4630 mm³, which covers the required 40x40 area minus mounting holes.
- R4: PASS. Measured $R = 6.991$ K/W (<= 9 K/W).
- R5: FAIL. The simulation reports `empty_ratio: 0.0` and `walled_ratio: 0.521` for the holes. This indicates that while the mounting holes exist in the base, there is material present above the base ($z \ge 3$) at the hole locations, preventing screwdriver access. The requirement specifies no material within 3 mm of the axis for $z \ge 3$.
- R6: PASS. Measured mass is 42.59 g (<= 45 g).

## Verdicts
R1: PASS - Single solid confirmed by simulation.
R2: PASS - Footprint 40x40 mm and height 23 mm meet limits.
R3: PASS - Base thickness from z=0 to z=3 is verified.
R4: PASS - Measured R = 6.991 K/W is <= 9 K/W.
R5: FAIL - Simulation shows material exists above the base at the mounting hole locations (walled_ratio > 0), violating screwdriver clearance.
R6: PASS - Measured mass 42.59 g is <= 45 g.

## Problems
- R5: Screw clearance voids - Material exists within the clearance zone for $z \ge 3$ at $(\pm 15, 0)$.

SIM_CODE_ISSUE: no