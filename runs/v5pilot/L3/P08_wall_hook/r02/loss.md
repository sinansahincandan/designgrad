## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: PASS - Plate dimensions match $x \in [0, 2], |y| \le 8, z \in [-5, 45]$.
R3: FAIL - Only one hole found at (1, 0, 20) instead of two; also plate thickness (2mm) is less than required 4mm.
R4: PASS - Bed and pocket volumes match specification.
R5: PASS - Lip volume matches specification.
R6: PASS - Stress (0.57 MPa) < 25 MPa and deflection (0.003 mm) < 1.5 mm.
R7: PASS - Mass (18.06 g) < 25 g and X-extent (52 mm) < 55 mm.

## Problems
- R3: Screw holes; found one hole at (y,z)=(0,20) instead of two holes at (0,0) and (0,40).
- R3: Plate thickness; current thickness is 2mm, must be $\ge$ 4mm around holes.

SIM_CODE_ISSUE: yes