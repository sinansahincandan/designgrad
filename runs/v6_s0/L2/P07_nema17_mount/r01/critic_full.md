## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The requirement specifies a face plate from $y=0$ to $4$ with solid material all around the central bore. Simulation shows an intersection volume ratio of only 0.199, meaning the face plate is mostly hollow or missing in that region.
- R3: FAIL. Requirement asks for a 22.5 mm diameter bore through the face plate. Simulation probe at $(0, y, 30)$ shows the cylinder is not empty (it contains material), indicating the hole was not cut correctly or the geometry is invalid.
- R4: FAIL. Simulation probe confirms the four motor screw holes are not present/empty as required.
- R5: PASS. Intersection volume with clearance box is 0.0, meaning no part of the bracket enters the forbidden motor zone.
- R6: FAIL. Simulation probe shows the two vertical screw holes at $(x=\pm 25, y=25)$ are not present/empty as required.
- R7: PASS. BBox and mass (38.93g) are within limits ($x \in [-35, 35]$, $z_{max} \le 55$, mass $\le 60$g).

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Intersection volume ratio is 0.199; face plate is not a solid block from y=0 to 4.
R3: FAIL - Cylinder probe shows the central bore is not empty.
R4: FAIL - Probed motor screw holes are not empty.
R5: PASS - Zero intersection with clearance volume.
R6: FAIL - Probed base screw holes are not empty.
R7: PASS - BBox and mass (38.93g) are within limits.

## Problems
- Face Plate Integrity: The face plate is missing most of its material in the $y=[0,4]$ region (volume ratio 0.199).
- Central Bore: The $\varnothing 22.5$ mm hole at $(0, y, 30)$ was not successfully cut.
- Motor Screw Holes: The four $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$ were not successfully cut.
- Base Screw Holes: The two $\varnothing 5.5$ mm holes at $(\pm 25, 25)$ were not successfully cut.

SIM_CODE_ISSUE: no