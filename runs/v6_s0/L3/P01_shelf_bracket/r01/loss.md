## Verdicts
R1: PASS - Simulation confirms one solid.
R2: FAIL - Y dimension is [-60, 20], exceeding requirement [-20, 20].
R3: PASS - Diameter and clearance requirements met per simulation.
R4: FAIL - Simulation indicates failure in support column fill and/or height constraints.
R5: PASS - Measured stress 0.275 MPa is $\le$ 20 MPa.
R6: PASS - Measured deflection 0.009 mm is $\le$ 2.0 mm.
R7: FAIL - Measured mass 534.08 g exceeds limit of 90 g.

## Problems
- Mass: Current mass is 534.08 g; must be $\le$ 90 g.
- Envelope (Y): Y range is [-60, 20]; must be within [-20, 20].
- Shelf Support/Height: Fails R4 constraints regarding material at $x \in [140, 150]$ and height for $x \ge 8$.

SIM_CODE_ISSUE: no