## Working
- R1: PASS. Evidence shows 1 solid found in STEP file.
- R2: PASS. Bounding box [0, 130], [-15, 15], [0, 20] is within limits (max x=136, |y|<=16, height<=20).
- R3: FAIL. Probed holes at (6, +-6) failed to find the required 3.2mm diameter holes.
- R4: FAIL. Simulation reports both motor holes and shaft hole are missing/incorrect.
- R5: FAIL. Measured stress is 428.57 MPa, which exceeds the limit of 30 MPa. (Note: The design document admits a massive failure here due to mathematical conflict).
- R6: FAIL. Requirement asks for $I \le 1.0$ at $x=20$. Simulation shows $I = 1.12$, which is $> 1.0$. Additionally, the deflection estimate (1020 mm) is physically absurd for a 130mm part, suggesting the geometry/simulation mismatch.
- R7: PASS. Measured mass is 16.27 g, which is $\le 20$ g.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Holes at (6, +-6) not found.
R4: FAIL - Motor and shaft holes not found.
R5: FAIL - Stress is 428.57 MPa (> 30 MPa).
R6: FAIL - I = 1.12 mm^4 (> 1.0 mm^4).
R7: PASS - Mass is 16.27 g (<= 20 g).

## Problems
- Strength: Bending stress at x=20 is 428.57 MPa, must be <= 30 MPa.
- Stiffness: Moment of inertia I at x=20 is 1.12 mm^4, must be <= 1.0 mm^4.
- Frame attachment: Vertical holes at (6, +-6) are missing or incorrectly sized.
- Motor mount: Four 3.2mm holes and one 6mm shaft hole are missing or incorrectly sized.

SIM_CODE_ISSUE: yes