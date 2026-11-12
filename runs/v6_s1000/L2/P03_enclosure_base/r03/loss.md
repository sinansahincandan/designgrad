## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor thickness and coverage verified by intersection volume.
R3: PASS - Cavity is completely free of material.
R4: PASS - Dimensions are 85x55x32 mm.
R5: FAIL - Bosses do not extend from the floor (start at z=4 instead of z=0) and pilot hole is not open at the top (hole_empty=0.0).
R6: PASS - Cutout dimensions and location verified.
R7: PASS - Mass 66.38g $\le$ 70g.

## Problems
- Bosses: Vertical extent is z=4 to z=8; should be z=0 to z=8.
- Pilot holes: Not open at the top of the boss (hole_empty = 0.0).

SIM_CODE_ISSUE: no