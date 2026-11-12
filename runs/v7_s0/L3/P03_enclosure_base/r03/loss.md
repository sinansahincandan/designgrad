## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness and coverage.
R3: PASS - Simulation confirms cavity is empty.
R4: PASS - Bounding box matches dimensions and height requirements.
R5: FAIL - Simulation probe failed to validate boss/hole geometry.
R6: FAIL - Render and simulation confirm the USB-C cutout is missing from the part.
R7: PASS - Mass is 36.37g, which is $\le$ 70g.

## Problems
USB-C Cutout: The opening at $x=-42.5, y=0, z=14$ is missing; it must be a through-cut in the $-X$ wall.
Screw Boss Pilot Holes: Simulation failed to validate boss/hole geometry.

SIM_CODE_ISSUE: no