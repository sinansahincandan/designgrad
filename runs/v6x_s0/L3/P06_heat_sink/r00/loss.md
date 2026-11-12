## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - BBox dimensions are $40 \times 40 \times 22$ mm and centered.
R3: PASS - Base volume matches expected thickness for the footprint.
R4: PASS - Measured $R = 7.218 \text{ K/W} \le 9$.
R5: FAIL - Simulation shows zero clearance volume; visual evidence shows pockets instead of vertical voids.
R6: PASS - Measured mass is 44.61 g $\le 45$ g.

## Problems
- R5: Screw clearance feature; current implementation uses small cylindrical pockets; must be a void with no material within 3 mm of the hole axis for all $z \ge 3$.

SIM_CODE_ISSUE: no