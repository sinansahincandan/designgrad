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