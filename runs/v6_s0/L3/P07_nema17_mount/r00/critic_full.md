## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Simulation shows shell fill ratio of 0.0 in the face plate region, and the visual reviewer notes the face plate is incorrectly oriented/sized.
- R3: FAIL. Simulation probe for the central bore returned 0.0 for both core and wall ratios, indicating the hole does not exist or is not positioned correctly.
- R4: FAIL. Simulation probe at motor screw locations failed to find holes.
- R5: PASS. Intersection volume with clearance box is 0.0.
- R6: FAIL. Simulation shows holes at (+-25, 25) do not exist; visual reviewer notes the base plate is in the negative Z region instead of $z \ge 0$.
- R7: PASS. BBox and mass (calculated as ~23.46g) are within limits.

## Verdicts
R1: PASS - Evidence from simulation confirms 1 solid.
R2: FAIL - Simulation shows 0.0 shell fill ratio; visual reviewer notes incorrect orientation/thickness.
R3: FAIL - Simulation probe shows no bore diameter at the specified location.
R4: FAIL - Simulation probe failed to find holes at motor screw locations.
R5: PASS - Intersection volume with clearance box is 0.0.
R6: FAIL - Simulation and visual review confirm base plate/holes are incorrectly located (negative Z).
R7: PASS - BBox and mass are within specification limits.

## Problems
- Orientation: Face plate is oriented in the XZ plane extending into negative Z; should be $y \in [0, 4]$.
- Base Plate Location: Located in negative Z region; should be at $z \ge 0$.
- Central Bore: Missing or incorrectly placed; should be $\varnothing 22.5$ mm at $(0, 30)$ through the face plate.
- Motor Screw Holes: Missing; should be four $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$.
- Base Screw Holes: Missing; should be two $\varnothing 5.5$ mm holes at $(\pm 25, 25)$.

SIM_CODE_ISSUE: no