## Working
- R1: PASS. Evidence confirms 1 solid.
- R2: FAIL. The bounding box y-range is [0.0, 40.0]. Requirement specifies -20 <= y <= 20. The part is offset from the center of the Y axis.
- R3: FAIL. Simulation shows "clear: false" regarding the 4mm clearance for x >= 10.
- R4: FAIL. Simulation indicates a fill ratio of 0.5 in the required region (x[140,150], y[-5,5], z[100,110]), meaning it does not provide solid material directly below z=110 as required.
- R5: PASS. Measured stress is ~0.27 MPa, which is <= 20 MPa. (Note: The simulation's $c$ and $I$ values differ significantly from the design doc estimates, but the result is well within limits).
- R6: PASS. Measured deflection is ~0.009 mm, which is <= 2.0 mm.
- R7: FAIL. Measured mass is ~180 g, which exceeds the limit of 90 g.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - y range [0, 40] does not fit within [-20, 20].
R3: FAIL - screwdriver clearance for x >= 10 is not met.
R4: FAIL - insufficient material below z=110 in the x[140,150] range.
R5: PASS - stress 0.27 MPa <= 20 MPa.
R6: PASS - deflection 0.009 mm <= 2.0 mm.
R7: FAIL - mass 180 g > 90 g.

## Problems
- Mass: Current mass is ~180 g, must be <= 90 g.
- Y-Envelope: y range is [0, 40], must be within [-20, 20].
- Shelf Support: Material at x[140,150] below z=110 has a fill ratio of only 0.5; must be solid material.
- Screwdriver Access: Clearance for x >= 10 is not met.

SIM_CODE_ISSUE: no