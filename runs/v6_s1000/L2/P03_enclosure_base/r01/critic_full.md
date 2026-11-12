## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Floor covers the board area from z=0 to z=2.
- R3: PASS. Board space is empty (0.0 mm³ material).
- R4: PASS. Dimensions are 85x55x32, within tolerances.
- R5: FAIL. The simulation probe for bosses shows `hole_empty: 0.0`. This indicates the pilot hole is not actually open/void at the top of the boss as required. The design document claims a subtraction from z=4 to z=8, but the evidence shows no void exists in the probed region.
- R6: PASS. Cutout volume and location are verified.
- R7: PASS. Mass is 66.389 g, which is $\le$ 70 g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor thickness and coverage verified.
R3: PASS - Board space is empty.
R4: PASS - Dimensions are 85 x 55 x 32 mm.
R5: FAIL - Probed bosses show no hole emptiness (hole_empty = 0.0).
R6: PASS - Cutout dimensions and location verified.
R7: PASS - Mass is 66.389 g.

## Problems
- R5: Screw bosses lack the required 2.2 mm pilot hole; simulation shows 0.0 mm³ empty volume in the hole region.

SIM_CODE_ISSUE: no