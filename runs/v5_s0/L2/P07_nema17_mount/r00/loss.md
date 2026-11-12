## Verdicts
R1: PASS - Evidence confirms 1 solid.
R2: FAIL - Annulus volume around bore is 0.0.
R3: FAIL - Bore volume at specified location is 0.0.
R4: UNSURE - Simulation measurement was not faithful to the geometry.
R5: PASS - Intersection volume with clearance box is 0.0.
R6: FAIL - $z_{min}$ is -27.5, violating the requirement that base be at $z \ge 0$.
R7: PASS - BBox and mass are within limits.

## Problems
- Base Position: $z_{min}$ is -27.5; should be $\ge 0$.
- Face Plate Integrity: Annulus volume around bore is 0.0; face plate must have solid material around the central bore (R2).
- Central Bore: Bore volume at $(0, 2, 30)$ is 0.0; bore must exist through the face plate (R3).

SIM_CODE_ISSUE: yes