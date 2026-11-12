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