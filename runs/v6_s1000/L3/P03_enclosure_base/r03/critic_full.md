## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms floor thickness/volume at $z=0$ to $2$.
- R3: PASS. Simulation confirms board cavity is empty.
- R4: PASS. Bounding box matches dimensions (85x55) and height ($z_{max}=32$).
- R5: FAIL. Simulation probe shows `hole_empty: 0.0`. This means the pilot hole was not actually subtracted/open at the top of the boss. The visual evidence also suggests bosses are not correctly formed as pillars rising to $z=8$.
- R6: FAIL. Simulation shows `empty_ratio: 0.0` for the cutout region, and the visual reviewer confirms the cutout is missing from the $-X$ wall.
- R7: PASS. Mass is measured at 66.521 g, which is $\le 70$ g. (Note: There is a massive discrepancy between the Design Doc estimate of 6g and the Simulation measurement of 66g due to volume units/calculation, but since $66.5 < 70$, it passes).

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