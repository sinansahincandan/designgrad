## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box x max is 150, but y range is [0, 40]. The requirement specifies -20 <= y <= 20 (a width of 40 centered at 0). The measured y range indicates the part is shifted or incorrectly sized relative to the Y-axis.
- R3: FAIL. Simulation reports "empty: 0.0" for holes and the visual reviewer notes screw holes are completely missing from the rendered part.
- R4: FAIL. Simulation reports `support_fill: 0.0`, meaning no material exists at z=110 between x=140 and 150. The visual reviewer also notes the shelf support is missing or incorrectly placed.
- R5: PASS. Measured stress is ~0.27 MPa, which is <= 20 MPa.
- R6: PASS. Measured deflection is ~0.009 mm, which is <= 2.0 mm.
- R7: FAIL. Measured mass is 124.18 g, which exceeds the limit of 90 g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Y range [0, 40] does not satisfy [-20, 20].
R3: FAIL - Screw holes are missing from the part.
R4: FAIL - No material found at z=110 for x in [140, 150].
R5: PASS - Measured stress 0.27 MPa <= 20 MPa.
R6: PASS - Measured deflection 0.009 mm <= 2.0 mm.
R7: FAIL - Mass 124.18 g > 90 g.

## Problems
- Mass: Current mass is 124.18 g, must be <= 90 g.
- Shelf Support: No material at z=110 between x=140 and x=150; must provide solid support at exactly z=110.
- Screw Holes: Holes are missing from the geometry; must include two 5.5 mm diameter holes at (y=0, z=20) and (y=0, z=60).
- Y-Axis Alignment: Y range is [0, 40], must be [-20, 20].

SIM_CODE_ISSUE: no