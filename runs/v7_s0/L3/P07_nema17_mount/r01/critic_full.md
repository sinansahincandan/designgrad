## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The reviewer notes the boundary check at $y=4$ fails and the ring walled ratio is 0.0. The render shows large cutouts that do not align with a continuous face plate of thickness 4mm.
- R3: FAIL. Simulation reports hit volume 0.0 for the bore probe, and the reviewer notes the bore is not visible in renders.
- R4: FAIL. Simulation only found 2 out of 4 holes ([0, 1, 0, 1]). The render does not show identifiable screw holes.
- R5: PASS. Simulation confirms 0.0 mm³ intersection with clearance volume.
- R6: FAIL. Measured $z_{min}$ is -27.5 mm; requirement specifies base on table ($z \ge 0$).
- R7: PASS. BBox and mass are within limits.

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