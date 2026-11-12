## Verdicts
R1: PASS - Simulation confirms one solid.
R2: FAIL - Bounding box y-range is [-10, 40], must be within [-20, 20].
R3: FAIL - Simulation indicates screw hole/clearance requirements not met.
R4: PASS - Top surface at z=110 and no material above for x>=8.
R5: PASS - Bending stress 0.26 MPa <= 20 MPa.
R6: PASS - Deflection 0.009 mm <= 2.0 mm.
R7: FAIL - Mass is 444.84 g, must be <= 90 g.

## Problems
- Mass: Current mass 444.84 g, should be <= 90 g.
- Envelope (Y): Y-range [-10, 40], should be within [-20, 20].
- Screw Access: Missing required screw holes and screwdriver clearance for x >= 10.

SIM_CODE_ISSUE: no