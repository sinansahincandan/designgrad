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