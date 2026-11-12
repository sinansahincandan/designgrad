## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection test shows floor area is covered from $z=0$ to $z=2$.
- R3: PASS. Intersection volume with the board space is 0.0, meaning it is empty.
- R4: PASS. Bounding box measurements (85x55x31) are within spec.
- R5: FAIL. Simulation probe for OD failed (`od_ok: false`). The visual reviewer also notes bosses are not visible in the cavity, suggesting they were either not modeled or incorrectly subtracted/merged. Even if the pilot hole depth is okay, the outer diameter fails.
- R6: FAIL. Simulation shows `opening_intersected: 0.0`, meaning the cutout does not actually intersect the wall (it failed to create an opening). The visual reviewer confirms the cutout is not visible in renders.
- R7: PASS. Mass is 65.43g, which is $\le$ 70g.

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