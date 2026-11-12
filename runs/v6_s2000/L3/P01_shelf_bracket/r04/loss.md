## Verdicts
R1: PASS - Simulation confirms one solid.
R2: FAIL - Y-dimension [-55, 25] exceeds required [-20, 20].
R3: FAIL - Screw holes and screwdriver clearance channels are missing.
R4: FAIL - Fill fraction at x[140,150] is 0.61 instead of 1.0.
R5: PASS - Measured stress 0.43 MPa $\le$ 20 MPa.
R6: PASS - Measured deflection 0.015 mm $\le$ 2.0 mm.
R7: FAIL - Mass is 93.0 g, exceeding the 90 g limit.

## Problems
- Screw holes and clearance channels (R3): Missing entirely from geometry.
- Shelf support (R4): Fill fraction at x[140,150] is 0.61; must be 1.0.
- Mass (R7): Measured mass is 93.0 g; must be $\le$ 90 g.
- Envelope (R2): Y-dimension is [-55, 25]; must be within [-20, 20].

SIM_CODE_ISSUE: no