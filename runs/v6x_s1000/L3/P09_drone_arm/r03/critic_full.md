## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Bounding box [0, 130], [-12, 12], [0, 15] is within limits [0, 136], [-16, 16], [0, 20].
- R3: FAIL. Simulation probe of holes at (6, ±6) failed/returned near-zero values, indicating the holes are not present or correctly located in the geometry.
- R4: FAIL. Simulation indicates both motor bolt holes and the shaft clearance hole are missing or incorrectly placed.
- R5: PASS. Measured stress is ~1.97 MPa, well below 30 MPa limit. (Note: The simulation $I$ value of 4499.20 contradicts the design document's claim of $I=1125$, but since the result is within limits, it passes).
- R6: PASS. Measured deflection estimate is ~0.25 mm. Note that the simulation uses an $I$ of 4499.20, which actually fails the requirement $I \le 1.0$. However, per instructions, I must follow the measured evidence. Wait—the requirement R6 says "I of the x=20 section <= 1.0 mm". The simulation reports $I=4499.20$ for the calculation. This means R6 is actually a FAIL because $4499.20 > 1.0$.
- R7: FAIL. Measured mass is 21.91 g, which exceeds the limit of 20 g.

Re-evaluating R6: The requirement is $I \le 1.0$. The simulation evidence for R6 says "Deflection estimate: 0.25 mm (I=4499.20)". Since $4499.20$ is not $\le 1.0$, the requirement is failed.

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