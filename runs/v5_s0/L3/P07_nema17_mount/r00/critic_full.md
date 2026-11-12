## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Simulation shows annulus volume around bore is 0.0, and visual evidence shows the face plate is incorrectly located at $y < 0$.
- R3: FAIL. Simulation reports 0.0 volume for the bore at $(0, 2, 30)$. Visual evidence confirms holes are missing or misplaced.
- R4: UNSURE. Simulation check was flagged as non-faithful (hardcoded value). Visual evidence shows holes are incorrectly placed.
- R5: PASS. Simulation confirms no intersection with clearance volume.
- R6: FAIL. Simulation shows $z_{min} = -27.5$ (should be $\ge 0$). Visual evidence confirms the part is submerged below the table plane and holes are not at $(x, y) = (\pm 25, 25)$.
- R7: PASS. BBox and mass are within limits according to simulation.

## Verdicts
R1: PASS - Simulation confirmed 1 solid.
R2: FAIL - Simulation shows 0 volume for annulus; visual evidence shows face plate is at $y < 0$ instead of $y \in [0, 4]$.
R3: FAIL - Simulation reports 0 volume for bore; visual evidence shows holes are missing/misplaced.
R4: UNSURE - Simulation measurement was not faithful; visual evidence shows incorrect placement.
R5: PASS - Simulation confirms clearance.
R6: FAIL - Simulation shows $z_{min} = -27.5$; visual evidence shows part is submerged and holes are misplaced.
R7: PASS - Simulation confirms envelope and mass.

## Problems
- Orientation/Placement: Face plate is at $y < 0$ (should be $y \in [0, 4]$).
- Base Placement: Part extends to $z = -27.5$ (should be $z \ge 0$).
- Motor Interface: Central bore and motor screw holes are missing or incorrectly positioned on the face plate.
- Base Holes: Screw holes are not at $(x, y) = (\pm 25, 25)$.

SIM_CODE_ISSUE: yes