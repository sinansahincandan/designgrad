## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Boundary check at y=4 failed and geometry does not match face plate description.
R3: FAIL - Simulation reports 0.0 hit volume for the central bore probe.
R4: FAIL - Simulation only detected 2 of the 4 required holes.
R5: PASS - Simulation confirms no intersection with clearance volume.
R6: FAIL - Measured z_min is -27.5 mm, violating the requirement to be on the table (z >= 0).
R7: PASS - BBox and mass are within specified limits.

## Problems
- Orientation/Placement: Part extends to $z = -27.5$ mm; should be $z \ge 0$.
- Face Plate: Geometry does not form a continuous plate at $y \in [0, 4]$ with solid material around the bore (R2).
- Central Bore: Bore is missing or incorrectly placed (R3).
- Motor Screw Holes: Only 2 holes detected instead of 4 (R4).

SIM_CODE_ISSUE: yes