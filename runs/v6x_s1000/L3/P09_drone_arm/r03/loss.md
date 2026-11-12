## Verdicts
R1: PASS - Found 1 solid.
R2: PASS - Bounding box within limits.
R3: FAIL - Holes at (6, +-6) not found/invalid.
R4: FAIL - Motor holes and shaft hole not found/invalid.
R5: PASS - Stress 1.97 MPa <= 30 MPa.
R6: FAIL - $I$ value of 4499.20 is > 1.0 mm.
R7: FAIL - Mass 21.91 g > 20 g.

## Problems
- R7: Mass is 21.91 g, must be <= 20 g.
- R6: Second moment of area $I$ is 4499.20 mm^4, must be <= 1.0 mm^4.
- R4: Motor mount holes (3.2 mm and 6 mm) are missing or incorrectly placed.
- R3: Frame attachment holes (3.2 mm) at (6, +-6) are missing or incorrectly placed.

SIM_CODE_ISSUE: no