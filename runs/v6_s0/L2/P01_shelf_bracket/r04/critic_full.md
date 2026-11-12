## Working
- R1: PASS. Evidence shows 1 solid.
- R2: FAIL. Measured Z max is 205.0 mm, which exceeds the limit of 130 mm. Measured Y range is [-15, 15], which fits within [-20, 20]. X range [0, 160] fits within [0, 170].
- R3: PASS. Screwdriver clearance and hole diameter verified by simulation.
- R4: FAIL. Simulation shows excess volume above z=110 for x>=8 (measured value 16265.96 mm³). The design intent claimed the top surface was capped at $z=110$, but the evidence proves geometry exists above this height.
- R5: PASS. Measured stress is ~0.41 MPa, well below 20 MPa. (Note: Simulation uses different M/c/I values than the text description, but both are < 20).
- R6: PASS. Measured deflection is ~0.013 mm, well below 2.0 mm.
- R7: FAIL. Measured mass is 121.75 g, which exceeds the limit of 90 g.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Z max is 205.0 mm (limit 130 mm).
R3: PASS - Clearance and diameter verified.
R4: FAIL - Excess volume above z=110 for x>=8.
R5: PASS - Stress is 0.41 MPa (limit 20 MPa).
R6: PASS - Deflection is 0.013 mm (limit 2.0 mm).
R7: FAIL - Mass is 121.75 g (limit 90 g).

## Problems
- Z-Height: Maximum Z is 205.0 mm, must be <= 130 mm.
- Top Surface Constraint: Geometry exists above z=110 for x>=8.
- Mass: Mass is 121.75 g, must be <= 90 g.

SIM_CODE_ISSUE: no