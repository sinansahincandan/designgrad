## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Material fraction around central bore is only 0.371, failing the "solid material all around" requirement.
R3: FAIL - Simulation shows empty volume fraction for the central bore at (0,0,30).
R4: FAIL - Simulation and visual inspection show incorrect implementation/presence of the four motor holes.
R5: PASS - No intersection with clearance zone.
R6: FAIL - Simulation shows $z_{min}$ issues and incorrect hole geometry at $(\pm 25, 25)$.
R7: PASS - Envelope and mass are within specification limits.

## Problems
- R3/R4 (Motor Holes): Central bore and motor screw holes are not correctly implemented as through-holes in the face plate.
- R6 (Base Holes): Vertical screw holes at $(\pm 25, 25)$ are missing or have incorrect diameter/placement.
- R2 (Face Plate Integrity): Insufficient material remains around the central bore.

SIM_CODE_ISSUE: no