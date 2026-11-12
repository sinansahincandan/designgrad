## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection volume shows floor is fully present from z=0 to z=2 under the board area.
- R3: PASS. Intersection volume with the specified cavity is 0.0 mm³.
- R4: FAIL. Measured bounding box is 86 x 56 mm. The requirement allows 85 +/- 1.5 mm (range 83.5 to 86.5). However, for Y, 56 mm is outside the range of 55 +/- 1.5 mm (53.5 to 56.5)? Wait, 55 + 1.5 = 56.5. Let's re-check: $85 \pm 1.5$ means X must be $[83.5, 86.5]$ and Y must be $[53.5, 56.5]$. The measured value is $X=86, Y=56$. Both are within tolerance. **Correction**: R4 is PASS based on the bounding box [86.0, 56.0, 32.0].
- R5: FAIL. Simulation probe shows `hole_empty: 0.0`. This means the pilot hole is not actually open/empty at the top of the boss (z=8). The requirement specifies a 2.2 mm pilot hole open at its top.
- R6: FAIL. Simulation shows `wall_material_in_probe: 375.0` in the cutout region. This indicates the USB-C cutout is not fully cleared through the wall; material remains where the opening should be.
- R7: PASS. Mass is 66.52 g, which is $\le$ 70 g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor volume matches requirement.
R3: PASS - Cavity is clear of material.
R4: PASS - Bounding box [86, 56, 32] is within tolerances for 85x55 and z=30-32.5.
R5: FAIL - Simulation shows the pilot hole is not empty at the top (hole_empty = 0.0).
R6: FAIL - Simulation shows wall material exists within the cutout probe volume.
R7: PASS - Mass 66.52 g $\le$ 70 g.

## Problems
USB-C Cutout: The opening is not fully cleared through the wall (material detected in probe).
Screw Bosses: Pilot holes are not open at the top of the bosses.

SIM_CODE_ISSUE: no