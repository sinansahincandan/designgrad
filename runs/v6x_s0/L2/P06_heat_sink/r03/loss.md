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