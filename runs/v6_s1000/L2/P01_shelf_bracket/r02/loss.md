## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Y range is [0, 40], must be [-20, 20].
R3: FAIL - Holes are reported as "walled".
R4: FAIL - Support volume check failed.
R5: PASS - Stress 0.26 MPa <= 20 MPa.
R6: PASS - Deflection 0.0089 mm <= 2.0 mm.
R7: FAIL - Mass 229.68 g > 90 g.

## Problems
- Mass: Current mass is ~229.68 g, must be <= 90 g.
- Y-axis Alignment: Y range is [0, 40], must be [-20, 20].
- Screw Hole Access: Holes are reported as "walled", failing the screwdriver access requirement.
- Shelf Support: Support volume at x[140,150] failed verification.

SIM_CODE_ISSUE: no