## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Intersection with specified box yields 98% volume ratio, confirming material presence in the required region.
- R3: FAIL. The simulation probe for holes at (0,0) and (0,40) returned "empty" values of ~0.8. This indicates the screw holes are not actually present or are not being detected as voids/holes through the plate.
- R4: PASS. Pocket emptiness and bed solidity verified by simulation.
- R5: PASS. Lip presence verified by intersection.
- R6: PASS. Stress (calculated from M*c/I) is within 25 MPa and deflection (0.007 mm) is well below 1.5 mm based on provided I and c values.
- R7: FAIL. Mass is measured at 29.83 g, which exceeds the limit of 25 g. X-extent is 52 mm, which is within the 55 mm limit.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Material exists in specified range [0,2]x[-8,8]x[-5,45].
R3: FAIL - Simulation probe indicates holes at (0,0) and (0,40) are not correctly formed/empty.
R4: PASS - Pocket is empty and bed is solid as required.
R5: PASS - Retaining lip material exists in specified range.
R6: PASS - Stress and deflection are within limits.
R7: FAIL - Mass is 29.83 g, which exceeds the limit of 25 g.

## Problems
- Mass: Current mass is 29.83 g; must be <= 25 g.
- Screw holes: Holes at (0,0) and (0,40) are not present or correctly formed in the back plate.

SIM_CODE_ISSUE: no