## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness/coverage.
R3: PASS - Simulation confirms board space is empty.
R4: PASS - Bounding box matches dimensions and height.
R5: FAIL - Simulation shows pilot holes are not open at the top.
R6: FAIL - Simulation and visual review confirm the cutout is missing.
R7: PASS - Measured mass 66.38 g $\le$ 70 g.

## Problems
- USB-C Cutout (R6): Missing from geometry; must be a $9 \times 3$ mm opening in the $-X$ wall at $y=0, z=14$.
- Screw Bosses (R5): Pilot holes are not open at the top ($z=8$); they must be accessible from the board side.

SIM_CODE_ISSUE: no