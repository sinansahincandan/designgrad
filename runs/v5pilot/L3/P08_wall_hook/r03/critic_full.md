## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Back plate dimensions and x-min are verified by simulation.
- R3: FAIL. Simulation reports 0 holes found. Visual evidence from the reviewer confirms the screw holes are missing in the rendered part (the plate is a solid vertical block).
- R4: FAIL. Simulation reports bed volume of 0.0 and pocket intersection of 0.0, meaning the strap seat geometry was not correctly implemented or subtracted.
- R5: PASS. Simulation confirms material exists in the specified lip region.
- R6: PASS. Simulation provides values for stress (0.18 MPa) and deflection (0.0006 mm) which are well within limits.
- R7: PASS. Mass is ~21.96 g (< 25 g) and X-extent is 52 mm (< 55 mm).

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