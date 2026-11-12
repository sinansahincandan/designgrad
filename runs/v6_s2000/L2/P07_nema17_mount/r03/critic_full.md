## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Face plate thickness is $y \in [0,4]$ and simulation shows material surrounding the bore.
- R3: FAIL. The probe at $(0, y, 30)$ with diameter 22.5 mm returned an empty value (0.0), meaning the central bore does not exist in the solid at that location.
- R4: FAIL. Simulation probed the four specified coordinates for $\varnothing 3.4$ mm holes and found 0/4 valid holes.
- R5: PASS. Interference volume with the motor clearance box is 0.0.
- R6: FAIL. While $z_{min}=0$ is correct, the simulation found 0 of the two required $\varnothing 5.5$ mm vertical holes at $(\pm 25, 25)$.
- R7: PASS. Bounding box $x \in [-35, 35]$, $z_{max} = 55$, and mass = 57.1 g (under 60 g limit).

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Plate thickness is 4mm and material exists around the bore.
R3: FAIL - Bore probe at $(0, y, 30)$ found no void/bore.
R4: FAIL - Probed coordinates for motor screw holes returned 0/4 valid holes.
R5: PASS - Interference volume with motor clearance zone is 0.0.
R6: FAIL - Simulation found 0 of the two required $\varnothing 5.5$ mm vertical holes.
R7: PASS - Envelope and mass are within limits (mass = 57.1 g).

## Problems
- Motor screw holes: 0/4 holes found at $(\pm 15.5, y, 30 \pm 15.5)$; 4 holes required.
- Central bore: No $\varnothing 22.5$ mm hole found at $(0, y, 30)$.
- Table mounting holes: 0/2 holes found at $(\pm 25, 25)$; 2 holes of $\varnothing 5.5$ mm required.

SIM_CODE_ISSUE: no