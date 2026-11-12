## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness and coverage.
R3: PASS - Simulation confirms cavity is empty.
R4: FAIL - Wall top at z=16.5; must be between 30 and 32.5. Floor is not at z=0.
R5: FAIL - Bosses are not correctly implemented/visible in the final geometry.
R6: FAIL - Cutout volume contains material (empty_ratio 0.0).
R7: PASS - Mass is ~34.9g.

## Problems
- Coordinate System: Floor is at z=-12.5; must be at z=0.
- Wall Height: Top of walls at z=16.5; must be between 30 and 32.5.
- USB-C Cutout: Opening is missing (material present); must be a void in the -X wall.
- Screw Bosses: Bosses are not correctly rendered/placed; must be solid cylinders at $(\pm35, \pm20)$ from z=2 to z=8 with pilot holes.

SIM_CODE_ISSUE: no