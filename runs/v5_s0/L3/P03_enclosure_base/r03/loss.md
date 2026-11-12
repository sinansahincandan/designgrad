## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Intersection volume shows floor exists under board area.
R3: PASS - Intersection volume with board space is 0.0.
R4: PASS - Bounding box matches dimensions and height.
R5: FAIL - Simulation probe failed for OD and hole depth; bosses are not visible in renders.
R6: PASS - Simulation confirms cutout volume is 0.0 (empty space).
R7: PASS - Mass is ~36.5g, which is <= 70g.

## Problems
- R5: Screw bosses: Bosses are missing or incorrectly modeled; they are not visible in renders and failed simulation probes for diameter and hole depth.

SIM_CODE_ISSUE: no