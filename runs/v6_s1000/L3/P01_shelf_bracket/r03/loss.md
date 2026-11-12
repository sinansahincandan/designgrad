## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Screw hole/clearance requirements not met per simulation.
R4: FAIL - Insufficient material below z=110 in the x=[140,150] range.
R5: PASS - Stress 0.27 MPa <= 20 MPa.
R6: PASS - Deflection 0.009 mm <= 2.0 mm.
R7: FAIL - Mass 209.13 g > 90 g.

## Problems
- Mass: Current mass is 209.13 g; must be <= 90 g.
- Shelf Support: Material density at x=[140,150], y=0, below z=110 is insufficient to meet R4.
- Screw Holes: Clearance/geometry for holes at (y=0, z=20) and (y=0, z=60) failed inspection.

SIM_CODE_ISSUE: no