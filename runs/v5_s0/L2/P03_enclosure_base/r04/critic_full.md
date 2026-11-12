## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection volume shows floor covers the full board area from $z=0$ to $z=2$.
- R3: PASS. Intersection volume with specified region is 0.0.
- R4: PASS. Bounding box matches 85x55mm and height 31mm (within 30-32.5 range).
- R5: FAIL. The simulation probe for the bosses failed on both OD and hole depth/diameter checks. Specifically, the pilot hole check (r=1.1, z:4-8) returned an empty ratio that indicates the requirement is not met. While the design document claims a 2.2mm diameter hole from $z=0$ to $z=8$, the simulation probe specifically failed these parameters.
- R6: PASS. Cutout volume in specified region is 0.0, confirming it is an opening.
- R7: PASS. Mass is 65.54g, which is $\le$ 70g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor covers board area from z=0 to z=2.
R3: PASS - Board space is completely free of material.
R4: PASS - Dimensions are 85x55x31 mm.
R5: FAIL - Boss pilot holes do not meet diameter or depth requirements per simulation probe.
R6: PASS - Cutout is present and correctly sized.
R7: PASS - Mass is 65.54g.

## Problems
- R5: Screw bosses pilot holes. The simulation failed to find the required 2.2 mm diameter hole with at least 4 mm depth at the top of the boss.

SIM_CODE_ISSUE: no