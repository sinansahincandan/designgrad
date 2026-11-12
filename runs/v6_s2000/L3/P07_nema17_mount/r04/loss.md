## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms material thickness around bore.
R3: FAIL - Simulation probe shows the central bore is not empty (walled).
R4: FAIL - Simulation and visual inspection confirm holes are missing or incorrectly placed.
R5: PASS - Simulation confirms no interference with motor volume.
R6: FAIL - Simulation and visual inspection confirm mounting holes are missing.
R7: PASS - Bounding box and mass are within limits.

## Problems
- Motor screw holes (R4): Found 0/4 or 2/4 holes; should have four $\varnothing 3.4$ mm holes at $(\pm 15.5, y, 30 \pm 15.5)$.
- Base mounting holes (R6): Holes are missing; should have two $\varnothing 5.5$ mm holes at $(x, y) = (\pm 25, 25)$.
- Central bore (R3): Bore is not empty/drilled through; should be a $\varnothing 22.5$ mm void at $(0, y, 30)$.

SIM_CODE_ISSUE: no