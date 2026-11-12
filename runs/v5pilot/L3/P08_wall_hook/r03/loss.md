## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Back plate geometry matches spec.
R3: FAIL - Simulation and visual evidence show zero screw holes present.
R4: FAIL - Simulation shows no strap bed or pocket volume exists at the specified coordinates.
R5: PASS - Retaining lip material is present.
R6: PASS - Stress and deflection are within limits.
R7: PASS - Mass and X-extent are within limits.

## Problems
- R3: Screw holes; 0 holes found, should have 2 holes at (0,0) and (0,40).
- R4: Strap seat; bed volume is 0.0 mm³, should have a solid bed at z = -14 under 34 <= x <= 46, |y| <= 4.

SIM_CODE_ISSUE: no