## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box y-range is [-55, 25], which exceeds the required [-20, 20].
- R3: FAIL. Simulation reports `clearance_vol: 0` and `empty_ratio: 0.0`, meaning the screw holes and screwdriver clearance channels are missing from the geometry. This is corroborated by the visual reviewer.
- R4: FAIL. Fill fraction in the shelf support region (x=140 to 150) is 0.61, but the requirement specifies solid material (fill fraction 1.0).
- R5: PASS. Measured stress $\sigma = 0.43$ MPa is $\le 20$ MPa.
- R6: PASS. Measured deflection $\delta = 0.015$ mm is $\le 2.0$ mm.
- R7: FAIL. Measured mass is 93.0 g, which exceeds the limit of 90 g.

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