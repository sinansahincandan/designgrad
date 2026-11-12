## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness and coverage.
R3: PASS - Simulation confirms cavity is clear.
R4: PASS - Bounding box matches dimensions.
R5: FAIL - Simulation shows pilot holes are not empty (hole_empty: 0.0).
R6: FAIL - Visual inspection shows the cutout is missing from the wall.
R7: PASS - Measured mass 66.38 g $\le$ 70 g.

## Problems
- R5: Screw bosses/pilot holes; hole emptiness is 0.0 (should be open at top).
- R6: USB-C cutout; missing from -X wall (should be a $9 \times 3$ mm opening).

SIM_CODE_ISSUE: no