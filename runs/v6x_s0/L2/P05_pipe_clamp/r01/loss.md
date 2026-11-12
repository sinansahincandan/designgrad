## Verdicts
R1: PASS - Counted 1 solid.
R2: FAIL - Y extent is 31.0 mm (required 18-22 mm).
R3: FAIL - Non-zero intersection volume with pipe cylinder (0.098).
R4: FAIL - Intersection volume with required band is near zero (0.0057).
R5: FAIL - Screw holes failed emptiness/material check.
R6: PASS - Flange geometry meets requirements.
R7: PASS - Mass is 10.12 g ($\le 25$ g).

## Problems
- Y-extent: Current width is 31.0 mm; must be between 18 and 22 mm.
- Pipe clearance: Material exists within the pipe radius (R=12.6); must be zero.
- Saddle band: No material found in the radial band 12.7 to 15.5 mm for $|x| \le 7$.
- Screw holes: Holes at $(\pm 27, 0)$ are not correctly implemented as empty vertical bores through the solid.

SIM_CODE_ISSUE: no