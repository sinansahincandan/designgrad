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