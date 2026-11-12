## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Footprint 40x40 mm and height 22 mm.
R3: PASS - Base thickness confirmed via intersection volume.
R4: PASS - $R = 7.218$ K/W $\le 9$ K/W.
R5: FAIL - `clearance_vol` is 0.0, meaning no screwdriver clearance exists above the holes.
R6: PASS - Mass 44.61 g $\le 45$ g.

## Problems
- R5: Screwdriver clearance; material exists within 3 mm of hole axes at $z \ge 3$. Clearance volume must be $> 0$.

SIM_CODE_ISSUE: no