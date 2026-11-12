## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - clearance_vol is 0 for x >= 10.
R4: FAIL - fill fraction in support zone is 0.8, not 1.0.
R5: PASS - sigma = 1.37 MPa <= 20 MPa.
R6: PASS - delta = 0.0377 mm <= 2.0 mm.
R7: PASS - mass = 42.85 g <= 90 g.

## Problems
- Screw Clearance (R3): The clearance volume for $x \ge 10$ is 0; it must be non-zero to allow screwdriver access.
- Shelf Support (R4): Fill fraction in the support zone ($x=140\text{--}150, y \approx 0, z \approx 110$) is 0.8; it must be 1.0 for a continuous solid surface.

SIM_CODE_ISSUE: no