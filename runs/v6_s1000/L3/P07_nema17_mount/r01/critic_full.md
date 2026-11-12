## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured thickness/material around central bore is insufficient (0.4 mm). The simulation shows the face plate does not have "solid material all around" the central bore as required.
- R3: FAIL. The central bore diameter is measured at 0.4 mm, whereas the requirement is 22.5 mm.
- R4: FAIL. The motor screw holes are measured with a diameter of 0.4 mm (requirement is 3.4 mm) and the visual review notes they are missing from the face plate entirely.
- R5: PASS. Intersection volume with clearance box is 0.0.
- R6: FAIL. Measured $z_{min}$ check failed, implying the base does not sit at $z=0$ or holes are incorrectly placed. The simulation shows hole empty/wall fractions of 0.072, indicating they are not correctly formed as $\varnothing 5.5$ mm holes.
- R7: FAIL. Envelope $z_{max}$ is 57.5 mm (requirement $\le 55$ mm). Mass calculation: Volume 35111.1 mm³ * 1.24 g/cm³ / 1000 = ~43.54 g. While mass is PASS, the envelope $z_{max}$ fails.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Measured material around central bore is only 0.4 mm; does not meet thickness/solid material requirements.
R3: FAIL - Measured diameter is 0.4 mm, requirement is 22.5 mm.
R4: FAIL - Measured diameter is 0.4 mm, requirement is 3.4 mm; holes are also visually missing.
R5: PASS - Intersection volume with clearance box is 0.0.
R6: FAIL - Simulation shows incorrect hole geometry and $z_{min}$ issues.
R7: FAIL - Top envelope $z_{max}$ is 57.5 mm, exceeding the 55 mm limit.

## Problems
- Central Bore (R3): Diameter is 0.4 mm; should be 22.5 mm.
- Motor Holes (R4): Diameter is 0.4 mm; should be 3.4 mm.
- Face Plate Material (R2): Insufficient material around central bore; requires solid material for $y \in [0, 4]$.
- Base Holes (R6): Incorrect geometry/placement; should be $\varnothing 5.5$ mm at $(x, y) = (\pm 25, 25)$.
- Envelope (R7): Top height is 57.5 mm; should be $\le 55$ mm.

SIM_CODE_ISSUE: no