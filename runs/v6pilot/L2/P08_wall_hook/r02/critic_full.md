## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Intersection with specified box [0,2]x[-8,8]x[-5,45] shows 98% volume match (solid material exists in the required range).
- R3: FAIL. The simulation probe for holes at (0,0) and (0,40) returned "empty: 1.0", meaning no hole was found at those coordinates. If the holes are missing, the requirement is not met.
- R4: PASS. Pocket emptiness and bed solidity verified by simulation.
- R5: PASS. Intersection with lip box confirms material presence.
- R6: PASS. Stress (0.13 MPa) and deflection are well within limits (25 MPa and 1.5 mm).
- R7: FAIL. Mass is measured at 34.87 g, which exceeds the limit of 25 g. X-extent is 52.0 mm, which is within the 55 mm limit.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Material exists in specified range [0,2]x[-8,8]x[-5,45].
R3: FAIL - Simulation probe indicates holes are missing at (0,0) and (0,40).
R4: PASS - Pocket emptiness and bed solidity verified.
R5: PASS - Material exists in specified lip range.
R6: PASS - Stress 0.13 MPa <= 25 MPa; deflection within limits.
R7: FAIL - Mass is 34.87 g, which exceeds the limit of 25 g.

## Problems
- Mass: Current mass is 34.87 g; must be <= 25 g.
- Screw holes: Holes at (0,0) and (0,40) are missing or not correctly placed.

SIM_CODE_ISSUE: no