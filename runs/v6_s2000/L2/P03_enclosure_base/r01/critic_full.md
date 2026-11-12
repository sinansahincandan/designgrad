## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Floor thickness is 8 mm (z=0 to z=8), which exceeds the 2 mm minimum.
- R3: PASS. Intersection volume with void box is 0.0.
- R4: PASS. Dimensions are 85 x 55 x 32 mm, within spec.
- R5: FAIL. The simulation probe at $(\pm 35, \pm 20)$ returned `false` for all four bosses (OD, hole, and wall checks). While the design document claims $\varnothing 7$ mm bosses with $2.2$ mm holes exist, the measured evidence shows they are not present or do not meet the geometry requirements at those coordinates.
- R6: PASS. Cutout is verified as empty and meets minimum dimensions.
- R7: PASS. Mass is 66.38 g, which is $\le 70$ g.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Floor thickness is 8 mm.
R3: PASS - Void region is empty.
R4: PASS - Dimensions are 85 x 55 x 32 mm.
R5: FAIL - Simulation probe at $(\pm 35, \pm 20)$ failed to detect the bosses/holes.
R6: PASS - Cutout dimensions and location verified.
R7: PASS - Mass is 66.38 g.

## Problems
Screw Bosses: The four bosses at $(\pm 35, \pm 20)$ are missing or incorrectly modeled; simulation probe failed to detect OD, hole, or wall presence.

SIM_CODE_ISSUE: no