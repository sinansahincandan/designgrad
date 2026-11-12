## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Intersection volume ratio is 1.0 for the specified floor area.
- R3: PASS. Intersection volume with board space is 0.0.
- R4: PASS. Bounding box [85, 55] and zmax=31 are within spec.
- R5: FAIL. The simulation probe for the bosses at (+-35, +-20) returned `false` for all four bosses regarding OD or hole depth. Specifically, the hole depth probe (r=1.1, z:4-8) failed to find the required empty volume. The design document claims a 6mm deep hole from $z=8$ down to $z=2$, but the simulation indicates the holes are not meeting the requirement (either diameter or depth).
- R6: PASS. Cutout probe shows 0.0 intersection volume, meaning the cutout exists as intended.
- R7: PASS. Mass is 65.54g, which is $\le$ 70g.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Floor thickness and coverage verified by intersection volume.
R3: PASS - Board space is completely free of material.
R4: PASS - Dimensions [85, 55] and height 31 are within spec.
R5: FAIL - Simulation probe failed for all four bosses regarding OD or hole depth.
R6: PASS - Cutout volume is 0.0 (empty) and wall presence is confirmed.
R7: PASS - Mass 65.54g $\le$ 70g.

## Problems
- R5: Screw Bosses: Pilot holes do not meet the depth or diameter requirements at $(\pm35, \pm20)$ per simulation probe.

SIM_CODE_ISSUE: no