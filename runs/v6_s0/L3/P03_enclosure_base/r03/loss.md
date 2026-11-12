## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Intersection test confirms floor thickness and coverage.
R3: PASS - Intersection volume with board space is 0.0.
R4: PASS - Bounding box dimensions are within tolerance.
R5: FAIL - Measured outer diameter of bosses does not meet the $\ge$ 6 mm requirement.
R6: FAIL - Cutout does not intersect the wall, resulting in no opening.
R7: PASS - Mass is 65.43 g, which is $\le$ 70 g.

## Problems
- R6: USB-C cutout; opening size/intersection is 0 mm (no hole created), should be at least 9 mm wide and 3 mm high through the wall.
- R5: Screw bosses; outer diameter is < 6 mm, should be $\ge$ 6 mm.

SIM_CODE_ISSUE: no