## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms material exists in $y \in [0,4]$ around the bore.
- R3: FAIL. Simulation probe at $(0, y, 30)$ with diameter 22.5 mm returns a value of ~0.4 mm (walled), meaning the hole is not actually empty/drilled through as required.
- R4: FAIL. Simulation found 0 out of 4 holes. Visual inspection confirms only two holes exist at $z=44.5$, failing both count and position requirements $(\pm 15.5, 30 \pm 15.5)$.
- R5: PASS. Simulation shows zero interference with the motor clearance volume.
- R6: FAIL. Simulation reports 0/2 holes found. Visual inspection confirms base mounting holes are missing.
- R7: PASS. Bounding box and mass (57.0g) are within limits ($x \in [-35, 35]$, $z_{max} \le 55$, mass $\le 60$g).

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