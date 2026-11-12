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