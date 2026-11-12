## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Intersection test confirms floor thickness and area.
R3: PASS - Intersection test confirms cavity is empty.
R4: PASS - Bounding box matches dimensions.
R5: FAIL - Simulation probe failed for OD and pilot hole depth/diameter.
R6: FAIL - Simulation shows the cutout does not intersect the opening; visual evidence suggests incorrect placement.
R7: PASS - Mass 65.47g is within limit.

## Problems
- R6: USB-C Cutout: The cutout does not create an opening to the cavity (opening_intersected = 0) and is incorrectly positioned on the face/corner rather than centered at $y=0$ on the $-X$ wall.
- R5: Screw Bosses: Pilot holes do not meet diameter or depth requirements, and outer diameters are incorrect.

SIM_CODE_ISSUE: no