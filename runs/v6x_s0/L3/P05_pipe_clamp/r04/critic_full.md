## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. BBox shows Y extent = 31 mm (required 18-22 mm) and Zmin = -27.5 (required z=0). X extent is 31 mm (<= 80 mm is OK, but the geometry is fundamentally misplaced/wrongly sized).
- R3: PASS. Intersection volume with pipe cylinder is near zero.
- R4: FAIL. Measured intersection volume of required shell band is 0.0. The render shows the saddle is oriented vertically along Z instead of horizontally along Y.
- R5: FAIL. Simulation confirms holes are not empty/present at (+-27, 0). Render shows screw holes are missing.
- R6: FAIL. Measured intersection with flange probe boxes is false. Design document claims flanges exist, but render and simulation show they are missing.
- R7: PASS. Mass is ~1.75 g (<= 25 g).

## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: FAIL - Y extent is 31 mm (req 18-22) and Zmin is -27.5 (req 0).
R3: PASS - Pipe volume is free of material.
R4: FAIL - Required shell band contains no material at |x| <= 7.
R5: FAIL - Screw holes are not present/empty at (+-27, 0).
R6: FAIL - Flange volumes are missing.
R7: PASS - Mass is ~1.75 g (req <= 25 g).

## Problems
- Orientation/Placement: Saddle axis is along Z; must be along Y. Part sits at z=-27.5; must sit on z=0.
- Dimensions: Y extent is 31 mm; should be 18-22 mm.
- Missing Features: Base plate, flanges (R6), and screw holes (R5) are missing from the geometry.
- R4 Coverage: The saddle band does not exist in the required region.

SIM_CODE_ISSUE: no