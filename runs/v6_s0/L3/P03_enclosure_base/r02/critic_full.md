## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms floor covers the board area from z=0 to 2.
- R3: PASS. Simulation confirms the specified cavity is empty of material.
- R4: PASS. Bounding box measurements (85x55, zmax=31) meet requirements.
- R5: FAIL. Simulation probe for OD at $(\pm35, \pm20)$ returned `od_ok: false`. While the design document claims $OD=6\text{mm}$, the simulation evidence shows the measured diameter is incorrect. The reviewer also noted bosses are not visible in renders.
- R6: FAIL. Simulation reports `opening_intersected: 0.0`, meaning the cutout does not actually intersect/penetrate the wall as required. This matches the reviewer's observation that the cutout is not visible on the $-X$ wall.
- R7: PASS. Mass is $65.43\text{g}$, which is $\le 70\text{g}$.

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