## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms floor thickness/coverage.
- R3: PASS. Simulation confirms board space is empty.
- R4: PASS. Bounding box measurements (85x55, zmax=31) match requirements.
- R5: FAIL. Simulation reports `od_ok: false`. The reviewer notes the bosses appear as holes/indentations rather than 6mm OD pillars. This contradicts the requirement for solid round bosses with a pilot hole.
- R6: FAIL. Simulation shows `opening_intersected: 0.0` (no opening found) and the reviewer confirms the cutout is missing from the renders. Even though void volume was detected, it did not create an opening in the wall.
- R7: PASS. Mass is 65.43g, which is $\le$ 70g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness and coverage.
R3: PASS - Simulation confirms board space is empty.
R4: PASS - Bounding box matches dimensions and height.
R5: FAIL - Measured OD is less than 6mm; bosses appear as holes rather than pillars.
R6: FAIL - Cutout does not create an opening in the wall (opening_intersected = 0).
R7: PASS - Mass of 65.43g is within limit.

## Problems
- R6: USB-C cutout; no opening created in the -X wall.
- R5: Screw bosses; outer diameter is < 6 mm (appears as holes/indentations instead of solid pillars).

SIM_CODE_ISSUE: no