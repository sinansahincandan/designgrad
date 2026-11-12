## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Floor thickness and coverage verified by intersection check.
- R3: PASS. Intersection with board cavity volume is 0.0, meaning the space is clear.
- R4: PASS. Bounding box measurements (85x55x31) are within specification limits.
- R5: FAIL. Simulation probe for the four bosses at $(\pm35, \pm20)$ returned `od_ok: false` and `hole_ok: false`. While the design document claims OD=7mm and 4mm depth, the measured evidence shows they do not meet the requirement.
- R6: FAIL. Simulation reports `opening_intersected: 0.0`, meaning the cutout does not actually intersect/penetrate the wall to create an opening. The void volume exists, but it is not a valid opening in the side wall.
- R7: PASS. Mass is measured at 65.5g, which is $\le$ 70g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor thickness and coverage verified.
R3: PASS - Board cavity volume intersection is 0.0.
R4: PASS - Bounding box dimensions are within spec.
R5: FAIL - Probed bosses failed both outer diameter and pilot hole requirements.
R6: FAIL - Cutout does not intersect the wall to create an opening (opening_intersected = 0.0).
R7: PASS - Mass is 65.5g, which is $\le$ 70g.

## Problems
- USB-C Cutout: The cutout fails to penetrate the $-X$ wall, resulting in no actual opening.
- Screw Bosses: The bosses at $(\pm35, \pm20)$ fail both the outer diameter and pilot hole requirements.

SIM_CODE_ISSUE: no