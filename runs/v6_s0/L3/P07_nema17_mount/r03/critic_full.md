## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms material integrity around $y \in [0,4]$.
- R3: FAIL. Simulation says PASS (diameter 22.5), but the visual reviewer notes a diameter of 3.4 mm and that the central bore is missing/replaced by the clearance volume. The simulation probe likely failed to distinguish between the intended bore and the clearance cutout.
- R4: FAIL. Simulation says FAIL. Visual reviewer confirms holes are at $z=18$ instead of the required $z \in \{14.5, 45.5\}$.
- R5: PASS. Simulation confirms zero intersection with clearance volume.
- R6: FAIL. Simulation says FAIL (holes not found). Visual reviewer notes holes are located at $y=48.25$, which is near the edge of the plate, and implies they may not be correctly placed or sized relative to the base.
- R7: PASS. BBox and mass are within limits.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms material integrity in face plate.
R3: FAIL - Visual evidence shows diameter is 3.4 mm instead of 22.5 mm; central bore is missing.
R4: FAIL - Holes are at $z=18$ instead of $z=14.5$ and $z=45.5$.
R5: PASS - Simulation confirms clearance volume is empty.
R6: FAIL - Simulation failed to find the holes; visual evidence suggests incorrect placement/existence.
R7: PASS - Envelope and mass are within limits.

## Problems
- R3: Central bore diameter is 3.4 mm, should be 22.5 mm.
- R4: Motor hole Z-coordinates are at $z=18$, should be at $z=14.5$ and $z=45.5$.
- R6: Base holes not detected by simulation/incorrectly placed.

SIM_CODE_ISSUE: yes