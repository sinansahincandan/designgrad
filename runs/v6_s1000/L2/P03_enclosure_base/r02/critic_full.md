## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection volume shows floor is fully present from z=0 to z=2 under the board area.
- R3: PASS. Intersection volume with the specified cavity is 0.0 mm³.
- R4: PASS. Bounding box dimensions (85x55) and Z-height (32) match requirements.
- R5: FAIL. The design document states pilot holes are created by subtracting cylinders from $z=3.5$ to $z=8$. This means the hole is *not* open at the top ($z=8$), as it only exists between 3.5 and 8. The simulation probe confirms `hole_empty: 0.0`, meaning the hole is not empty/open at the required location.
- R6: FAIL. Simulation shows `wall_material_in_probe: 307.5` within the cutout volume, indicating the cutout did not successfully remove the wall material or was incorrectly positioned/sized. The design document claims a $9 \times 3$ mm cutout at $x=-42.5$, but the simulation evidence shows the probe box is not empty.
- R7: PASS. Mass is 66.38 g, which is $\le 70$ g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor volume matches requirement.
R3: PASS - Cavity is empty.
R4: PASS - Dimensions and height are within spec.
R5: FAIL - Pilot holes are not open at the top (z=8) as they only extend from z=3.5 to z=8.
R6: FAIL - Simulation shows significant wall material remains in the cutout probe volume.
R7: PASS - Mass is 66.38 g.

## Problems
- USB-C Cutout: The R6 cutout fails to clear the wall material (simulation shows 307.5 mm³ of material remaining).
- Screw Boss Pilot Holes: The holes are not open at the top; they extend from $z=3.5$ to $z=8$, leaving the top surface solid. They must be open at $z=8$.

SIM_CODE_ISSUE: no