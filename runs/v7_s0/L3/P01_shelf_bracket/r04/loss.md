## Verdicts
R1: PASS - Simulation confirms one solid.
R2: FAIL - Z-dimension reaches 216 mm, exceeding the limit of 130 mm.
R3: FAIL - Simulation shows screw holes and clearance access do not exist.
R4: FAIL - No material found at the required shelf support location; part exceeds $z=110$ for $x \ge 8$.
R5: PASS - Measured stress is 0.55 MPa.
R6: PASS - Measured deflection is 0.02 mm.
R7: PASS - Measured mass is 61.11 g.

## Problems
- Shelf Support (R4): The arm is angled upwards/incorrectly positioned; fill fraction at $z \in [105, 110], x \in [140, 150]$ is 0.0 instead of $\ge 1.0$.
- Envelope (R2): Z-dimension is 216 mm, should be $\le 130$ mm.
- Screw Holes (R3): Holes and clearance access are missing from the geometry.
- Height Constraint (R4): Material exists above $z=110$ for $x \ge 8$.

SIM_CODE_ISSUE: no