## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - z-max is 205 mm, exceeding 130 mm.
R3: PASS - holes and clearance verified.
R4: FAIL - geometry violates height constraints or support requirements for $x \ge 8$.
R5: PASS - stress is 0.41 MPa $\le$ 20 MPa.
R6: PASS - deflection is 0.013 mm $\le$ 2.0 mm.
R7: FAIL - mass is 135.23 g, exceeding 90 g.

## Problems
- Height Violation: The part reaches $z=205$ mm; it must not exceed $z=130$ mm.
- Mass Violation: Mass is 135.23 g; it must be $\le$ 90 g.
- Z-Constraint/Support Violation: Geometry for $x \ge 8$ violates the $z \le 110$ limit or the required support at $x \in [140, 150]$.

SIM_CODE_ISSUE: no