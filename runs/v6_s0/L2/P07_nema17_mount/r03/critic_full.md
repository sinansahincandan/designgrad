## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The intersection volume ratio in the face plate region ($y \in [0,4]$) is only 0.169, indicating the face plate is not a continuous solid of at least 4mm thickness as required.
- R3: FAIL. Probing the central bore shows it is empty (0.0) or contains negligible material, meaning the hole was not successfully cut through the face plate or the geometry is incorrect.
- R4: FAIL. Probe failed to find the four $\varnothing 3.4$ mm holes at the specified coordinates.
- R5: PASS. Intersection volume with the clearance box is 0.0.
- R6: FAIL. Probe failed to find the two $\varnothing 5.5$ mm vertical screw holes at $(\pm 25, 25)$.
- R7: PASS. BBox $x \in [-35, 35]$, $z_{max} = 27.5$, and mass is within limits.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Intersection volume ratio (0.169) indicates the face plate does not meet the 4mm thickness requirement.
R3: FAIL - Probing shows no valid $\varnothing 22.5$ mm bore at $(0, y, 30)$.
R4: FAIL - Probing failed to find the four $\varnothing 3.4$ mm motor screw holes.
R5: PASS - No intersection with the motor clearance volume.
R6: FAIL - Probing failed to find the two $\varnothing 5.5$ mm base screw holes.
R7: PASS - Envelope and mass are within specification.

## Problems
- Face Plate Thickness: The face plate material in $y \in [0,4]$ is insufficient (ratio 0.169); it must be a solid 4mm thick.
- Central Bore: The $\varnothing 22.5$ mm bore at $(0, y, 30)$ is missing or incorrectly implemented.
- Motor Screw Holes: The four $\varnothing 3.4$ mm holes at $(\pm 15.5, y, 30 \pm 15.5)$ are missing or incorrectly implemented.
- Base Screw Holes: The two $\varnothing 5.5$ mm holes at $(x, y) = (\pm 25, 25)$ are missing or incorrectly implemented.

SIM_CODE_ISSUE: no