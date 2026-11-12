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