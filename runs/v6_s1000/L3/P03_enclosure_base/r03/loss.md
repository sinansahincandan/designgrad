## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness.
R3: PASS - Simulation confirms board cavity is empty.
R4: PASS - Bounding box matches specification.
R5: FAIL - Simulation shows pilot holes are not open at the top (`hole_empty: 0.0`).
R6: FAIL - Simulation and visual inspection confirm the USB-C cutout is missing.
R7: PASS - Measured mass (66.521 g) is under 70 g.

## Problems
- R6: USB-C Cutout; opening is missing from the $-X$ wall.
- R5: Screw Bosses; pilot holes are not open at the top of the bosses.

SIM_CODE_ISSUE: no