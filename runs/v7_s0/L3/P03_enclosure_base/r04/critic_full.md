## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms floor covers the board area from z=0 to z=2.
- R3: PASS. Simulation confirms the specified cavity volume is empty.
- R4: FAIL. Measured Z-max is 16.5 mm, which is below the required range of 30–32.5 mm. The bounding box also shows a Z-min of -12.5, violating the requirement that the floor is at z=0.
- R5: FAIL. Although the design document claims bosses exist, simulation and visual review indicate they are either incorrectly placed (submerged) or not present in the final geometry. The pilot hole depth/placement is also suspect given the Z-coordinate shift.
- R6: FAIL. Simulation shows `empty_ratio: 0.0` for the cutout volume, meaning no material was removed to create the opening. Visual review confirms the cutout is missing.
- R7: PASS. Measured mass is ~34.9g, which is $\le$ 70g.

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