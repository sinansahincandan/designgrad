## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection volume shows floor is fully present from z=0 to z=2 under the board area.
- R3: PASS. Intersection volume with the specified cavity is 0.0 mm³.
- R4: PASS. Bounding box matches 85x55mm and wall height is 32mm (within 30-32.5 range).
- R5: FAIL. The design document states bosses extend from $z=4$ to $z=8$. However, the requirement R5 specifies bosses must be "from the floor up to z = 8". Since the floor is at $z=0$, a boss starting at $z=4$ leaves a gap between the floor and the boss. Furthermore, simulation probe `hole_empty: 0.0` indicates the pilot hole is not actually empty/open at the top of the boss as required.
- R6: PASS. Cutout dimensions (9mm Y, 3mm Z) are met by the subtraction volume (-4.5 to 4.5 = 9mm; 12.5 to 15.5 = 3mm).
- R7: PASS. Mass is 66.38g, which is $\le$ 70g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor thickness and coverage verified by intersection volume.
R3: PASS - Cavity is completely free of material.
R4: PASS - Dimensions are 85x55x32 mm.
R5: FAIL - Bosses do not extend from the floor (start at z=4 instead of z=0) and pilot hole is not open at the top (hole_empty=0.0).
R6: PASS - Cutout dimensions and location verified.
R7: PASS - Mass 66.38g $\le$ 70g.

## Problems
- Bosses: Vertical extent is z=4 to z=8; should be z=0 to z=8.
- Pilot holes: Not open at the top of the boss (hole_empty = 0.0).

SIM_CODE_ISSUE: no