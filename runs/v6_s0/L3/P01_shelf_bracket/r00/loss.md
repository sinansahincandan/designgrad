## Verdicts
R1: PASS - 1 solid detected.
R2: FAIL - y-range [0, 30] violates [-20, 20].
R3: FAIL - Holes are oriented along Z instead of X; centers at (y=1.75, z=35/75) violate (y=0, z=20/60).
R4: FAIL - Material exists above z=110 for x>=8 and insufficient support at x[140, 150].
R5: PASS - Stress 0.378 MPa <= 20 MPa.
R6: PASS - Deflection 0.012 mm <= 2.0 mm.
R7: FAIL - Mass 119.34g exceeds 90g limit.

## Problems
- Screw Holes: Axis is along Z, should be along X; centers are at (y=1.75, z=35) and (y=1.75, z=75), should be (y=0, z=20) and (y=0, z=60).
- Mass: 119.34g exceeds 90g limit.
- Envelope: y-range is [0, 30], should be within [-20, 20].
- Shelf Support: Material exists above z=110 for x>=8; support at x[140, 150] is insufficient.

SIM_CODE_ISSUE: no