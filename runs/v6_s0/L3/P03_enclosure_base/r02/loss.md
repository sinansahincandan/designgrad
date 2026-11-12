## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness and coverage.
R3: PASS - Simulation confirms cavity is empty.
R4: PASS - Bounding box matches dimensions and height.
R5: FAIL - Measured OD at $(\pm35, \pm20)$ does not meet the $\ge 6\text{mm}$ requirement (Evidence R5).
R6: FAIL - Cutout does not intersect the wall (Evidence R6); cutout is not visible in renders.
R7: PASS - Mass $65.43\text{g} \le 70\text{g}$.

## Problems
- USB-C Cutout (R6): Opening does not penetrate/intersect the $-X$ wall; should have a void intersecting the wall at $y=0, z=14$.
- Screw Bosses (R5): Outer diameter is less than 6 mm.

SIM_CODE_ISSUE: no