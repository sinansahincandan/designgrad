## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - y range [0, 40] does not fit within [-20, 20].
R3: FAIL - screwdriver clearance for x >= 10 is not met.
R4: FAIL - insufficient material below z=110 in the x[140,150] range.
R5: PASS - stress 0.27 MPa <= 20 MPa.
R6: PASS - deflection 0.009 mm <= 2.0 mm.
R7: FAIL - mass 180 g > 90 g.

## Problems
- Mass: Current mass is ~180 g, must be <= 90 g.
- Y-Envelope: y range is [0, 40], must be within [-20, 20].
- Shelf Support: Material at x[140,150] below z=110 has a fill ratio of only 0.5; must be solid material.
- Screwdriver Access: Clearance for x >= 10 is not met.

SIM_CODE_ISSUE: no