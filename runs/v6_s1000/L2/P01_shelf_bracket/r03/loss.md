## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - y range is [-25, 25], must be within [-20, 20].
R3: UNSURE - simulation check failed/was unfaithful.
R4: FAIL - material detected above z=110 for x >= 8.
R5: PASS - stress is 0.225 MPa <= 20 MPa.
R6: PASS - deflection is 0.007 mm <= 2.0 mm.
R7: FAIL - mass is 274.35 g, must be <= 90 g.

## Problems
- Mass: current mass is 274.35 g, should be <= 90 g.
- Envelope: y-dimension is [-25, 25], should be within [-20, 20].
- Shelf Profile: material exists above z=110 for x >= 8, should have nothing above z=110 for x >= 8.

SIM_CODE_ISSUE: no