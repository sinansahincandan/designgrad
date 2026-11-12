## Working
- R1: Evidence shows 1 solid. PASS.
- R2: BBox shows 40x40 mm footprint and 22 mm height. Centered on origin. PASS.
- R3: Intersection volume in $z=[0,3]$ matches the expected base volume (minus holes). This confirms a solid base of at least 3mm thickness over the footprint. PASS.
- R4: Measured $R = 7.218$ K/W, which is $\le 9$. PASS.
- R5: Simulation evidence for hole clearance shows `clearance_vol: 0.0` and `empty_ratio: 0.0`. This indicates that there is material within the required 3 mm radius of the hole axes above $z=3$, preventing screwdriver access. FAIL.
- R6: Measured mass is 44.61 g, which is $\le 45$ g. PASS.

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