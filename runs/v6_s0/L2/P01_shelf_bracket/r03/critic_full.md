## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The bounding box z-dimension reaches 205 mm, which exceeds the limit of 130 mm.
- R3: PASS. Screw holes and clearance requirements are met according to simulation probes.
- R4: FAIL. The simulation reports volume/geometry issues for $x \ge 8$ regarding height above $z=110$ or lack of support between $x=140$ and $150$. Specifically, the value `[0.0, 17949.8...]` suggests a failure in the check for material above $z=110$ or the required support column.
- R5: PASS. Stress $\sigma \approx 0.41$ MPa is well below the 20 MPa limit. (Note: The simulation uses different M/I values than the designer's estimate, but both pass).
- R6: PASS. Deflection $\delta \approx 0.013$ mm is well below the 2.0 mm limit.
- R7: FAIL. Measured mass is 135.23 g, which exceeds the 90 g limit.

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