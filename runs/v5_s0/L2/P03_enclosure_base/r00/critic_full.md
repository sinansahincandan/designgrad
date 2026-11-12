## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection volume ratio is 1.0 for the board footprint area from z=0 to 2.
- R3: PASS. Intersection volume with the specified board space is 0.0.
- R4: PASS. Bounding box measurements (85x55, zmax=31) are within spec limits.
- R5: FAIL. Simulation probe for the four bosses at (+-35, +-20) returned false for OD and hole depth requirements. The design document claims a 6mm OD and 4mm deep hole (z=4 to 8), but the measured evidence shows they do not meet these criteria.
- R6: UNSURE. The simulation check errored/was judged unfaithful; no valid measurement is provided for the cutout dimensions or position.
- R7: PASS. Mass is ~65.47g, which is $\le$ 70g.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Intersection volume ratio is 1.0.
R3: PASS - Intersection volume is 0.0.
R4: PASS - Bounding box [85, 55, 31] meets spec.
R5: FAIL - Measured probe failed for OD and hole depth at (+-35, +-20).
R6: UNSURE - Simulation check was unfaithful/errored.
R7: PASS - Mass is 65.47g $\le$ 70g.

## Problems
Bosses: Outer diameter < 6 mm and/or pilot hole depth < 4 mm at (+-35, +-20).

SIM_CODE_ISSUE: yes