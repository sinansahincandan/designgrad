## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The requirement specifies a solid floor at least 2mm thick under the whole board area (80x50). The simulation shows an intersection volume of ~7771 mm³ out of 8000 mm³, meaning material is missing from the floor region.
- R3: PASS. Intersection volume with the cavity is 0.0 mm³.
- R4: PASS. Bounding box matches dimensions (85x55) and height (32).
- R5: FAIL. Simulation probe shows `od_fill` of 0.863 (not a full solid cylinder) and `hole_empty` of 0.0 (the hole is not empty/open at the top). The visual evidence also confirms bosses are missing or not protruding.
- R6: FAIL. Simulation shows `wall_presence_vol` in the cutout area, meaning the wall is still there. Visual evidence confirms the cutout is completely missing.
- R7: PASS. Mass is 65.763 g, which is $\le$ 70 g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Intersection volume (7771 mm³) is less than required for a full 80x50x2 floor (8000 mm³).
R3: PASS - Cavity is completely free of material.
R4: PASS - Dimensions and height are within spec.
R5: FAIL - Bosses are not solid cylinders and the pilot holes are not empty/open at the top.
R6: FAIL - Cutout is missing from the wall.
R7: PASS - Mass (65.763 g) is under 70 g.

## Problems
- R6: USB-C cutout is missing; must provide a $9 \times 3$ mm opening in the $-X$ wall.
- R5: Screw bosses are not solid cylinders and pilot holes are not open at the top.
- R2: Floor thickness is insufficient/incomplete under the board area.

SIM_CODE_ISSUE: no