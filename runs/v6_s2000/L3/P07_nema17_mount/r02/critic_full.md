## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The simulation reports a plate volume of ~12409 mm³, which is massive for a 4mm thick face plate (a $50 \times 50 \times 4$ plate is only 10,000 mm³). More importantly, the "Wall ratio" of 0.400 suggests the material around the bore axis is not solid/continuous as required.
- R3: FAIL. The probe at (0, y, 30) shows 0.0 empty space and a wall ratio of 0.4, meaning the central bore is either missing or incorrectly placed/sized such that it does not exist as a through-bore on the axis.
- R4: FAIL. Simulation found 0 out of 4 holes at the specified coordinates. The visual reviewer also confirmed these holes are missing in the render.
- R5: PASS. Interference volume is 0.0, meaning the clearance zone is empty.
- R6: FAIL. Simulation shows 0/2 holes found at $(\pm 25, 25)$. Visual reviewer confirms they are missing.
- R7: PASS. Bounding box $x \in [-35, 35]$ and $z_{max} = 54$ fits the envelope. Mass is 56.7g, which is $\le 60$g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Simulation reports incorrect plate volume and insufficient material around bore axis.
R3: FAIL - Probe shows no valid central through-bore at (0, y, 30).
R4: FAIL - Simulation and visual review confirm motor screw holes are missing.
R5: PASS - Interference volume is 0.0.
R6: FAIL - Simulation and visual review confirm base mounting holes are missing.
R7: PASS - Envelope and mass (56.7g) are within limits.

## Problems
- Missing Fasteners: Motor screw holes (R4) are missing from the face plate.
- Missing Fasteners: Base mounting holes (R6) at $(\pm 25, 25)$ are missing.
- Central Bore: The $\varnothing 22.5$ mm bore (R3) is not present or correctly formed on the shaft axis.
- Face Plate Integrity: Material around the central bore (R2) does not meet thickness/solid requirements.

SIM_CODE_ISSUE: no