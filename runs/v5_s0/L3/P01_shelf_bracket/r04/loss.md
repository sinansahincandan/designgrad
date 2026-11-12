## Verdicts
R1: PASS - Simulation confirms one solid.
R2: PASS - BBox is within specified limits.
R3: FAIL - Screw hole centers and tool clearance do not meet specification.
R4: FAIL - Material exists above z=110 and top surface height/flatness is incorrect.
R5: PASS - Measured stress 0.54 MPa <= 20 MPa.
R6: PASS - Measured deflection 0.02 mm <= 2.0 mm.
R7: PASS - Measured mass 73.16 g <= 90 g.

## Problems
- Shelf support (z-height): Material exists above z=110; top surface is not at exactly z=110.
- Screw holes (position): Holes are centered at z≈15 and z≈55 instead of z=20 and z=60.
- Screw holes (clearance): Tool access clearance for x >= 10 is missing or incorrect.

SIM_CODE_ISSUE: no