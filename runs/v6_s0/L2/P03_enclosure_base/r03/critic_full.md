## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Floor thickness and coverage verified by intersection test.
- R3: PASS. Intersection volume with board space is 0.0.
- R4: PASS. Bounding box dimensions (85x55, zmax=31) are within spec.
- R5: FAIL. Simulation probe for the four bosses at $(\pm35, \pm20)$ returned `od_ok: false` and `hole_ok: false`. This indicates either the diameter is $<6\text{ mm}$ or the pilot hole does not meet the $2.2\text{ mm}$ diameter / $4\text{ mm}$ depth requirement.
- R6: FAIL. Simulation shows `opening_intersected: 0.0`, meaning the cutout did not actually intersect/remove material from the wall, despite the design document claiming it does.
- R7: PASS. Mass is $65.47\text{ g}$, which is $\le 70\text{ g}$.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Floor thickness and coverage verified.
R3: PASS - Board space is empty of material.
R4: PASS - Dimensions are within tolerance.
R5: FAIL - Probed bosses failed diameter and/or pilot hole depth requirements.
R6: FAIL - Cutout did not intersect the wall material.
R7: PASS - Mass is 65.47 g.

## Problems
- USB-C Cutout: The cutout fails to penetrate the $-X$ wall (opening_intersected = 0).
- Screw Bosses: The bosses fail diameter or pilot hole depth/diameter requirements.

SIM_CODE_ISSUE: no