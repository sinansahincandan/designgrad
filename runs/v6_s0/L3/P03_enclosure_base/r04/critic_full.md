## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Floor thickness and area verified by intersection test.
- R3: PASS. Board cavity volume is 0.0, meaning it is clear of material.
- R4: PASS. Bounding box measurements (85x55x31) are within spec.
- R5: FAIL. Simulation probe shows both OD and hole depth/diameter requirements failed for all four bosses. The design document claims a 4mm deep hole from $z=8$ to $z=4$, but the simulation reports `hole_ok: false`.
- R6: FAIL. Simulation shows `opening_intersected: 0.0`, meaning the cutout does not actually penetrate/open into the cavity or through the wall as required. The design document defines the cutout from $x=-42.5$ to $-37.5$, but since the inner boundary is at $x=-40$, this only penetrates 2.5mm into a wall that is likely thicker, failing to create an "opening" to the board space. Additionally, the visual reviewer notes it is not centered on the -X wall.
- R7: PASS. Mass is 65.47g, which is $\le$ 70g.

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