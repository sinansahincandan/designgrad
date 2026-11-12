## Verdicts
R1: PASS - Found 1 solid.
R2: PASS - Plate dimensions cover required range.
R3: FAIL - Simulation probe for hole emptiness/thickness returned 0.0.
R4: FAIL - Pocket volume probe returned 0.0, meaning the space is not empty.
R5: PASS - Lip volume matches requirement.
R6: PASS - Stress 1.43 MPa and deflection 0.015 mm are within limits.
R7: PASS - Mass 22.3 g and X-extent 52 mm are within limits.

## Problems
Strap Seat Pocket: Pocket volume is 0.0 mm³, should be at least $10 \times 12 \times 8 = 960$ mm³ (or specifically the specified volume).
Screw Holes: Hole emptiness/thickness probe returned 0.0, indicating holes are not correctly subtracted or positioned.

SIM_CODE_ISSUE: yes