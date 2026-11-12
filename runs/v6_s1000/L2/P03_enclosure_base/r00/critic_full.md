## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection volume shows floor is fully present from z=0 to z=2 under the board area.
- R3: PASS. Intersection volume with the specified cavity region is 0.0 mm³.
- R4: PASS. Bounding box measurements (85x55) and Z-max (32) match requirements.
- R5: FAIL. The simulation probe for bosses shows `hole_empty: 0.0`. This means the pilot hole is not actually empty/cut into the boss, violating the requirement for a 2.2 mm pilot hole.
- R6: PASS. Cutout volume and wall presence confirm the aperture exists at the correct location.
- R7: PASS. Mass is calculated as 66.246 g, which is $\le$ 70 g.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Floor thickness and coverage confirmed by intersection volume.
R3: PASS - Cavity is completely free of material.
R4: PASS - Dimensions (85x55) and wall height (32) are within spec.
R5: FAIL - Simulation probe shows the pilot hole is not empty (`hole_empty: 0.0`).
R6: PASS - Cutout dimensions and location verified.
R7: PASS - Mass of 66.246 g is $\le$ 70 g.

## Problems
- R5: Screw bosses lack the required 2.2 mm pilot holes (measured hole emptiness = 0.0).

SIM_CODE_ISSUE: no