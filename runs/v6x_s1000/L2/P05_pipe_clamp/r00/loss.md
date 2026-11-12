## Verdicts
R1: FAIL - Simulation detected 2 solids instead of 1.
R2: FAIL - Y extent is 43.5 mm (required 18-22 mm) and Zmin is -15.5 (must be 0).
R3: FAIL - Non-zero intersection volume (0.0484) indicates pipe volume is not free of material.
R4: PASS - Material exists in the specified band.
R5: FAIL - Intersection check shows holes are not correctly implemented at (+-27, 0).
R6: FAIL - Sampling shows 0.0 solid material in the required flange region.
R7: PASS - Mass is 18.813 g (<= 25 g).

## Problems
- R2: Clamp width (Y) is 43.5 mm; should be 18-22 mm.
- R2: Z minimum is -15.5 mm; should be 0.
- R6: Flanges are missing in the region |x| in [18.5, 23], |y|<=4, z in [0, 3].
- R3: Pipe volume contains material (intersection ratio 0.0484).
- R5: Screw holes at (+-27, 0) are not correctly formed.
- R1: Design consists of 2 separate solids instead of one.

SIM_CODE_ISSUE: no