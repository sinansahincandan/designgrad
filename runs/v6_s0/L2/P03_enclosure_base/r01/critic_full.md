## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Floor thickness and coverage verified by intersection test.
- R3: PASS. Board cavity is empty as per intersection volume = 0.0.
- R4: PASS. Bounding box dimensions (85x55) and height (31) are within spec.
- R5: FAIL. Simulation probe for the four bosses at $(\pm35, \pm20)$ returned `od_ok: false` and `hole_ok: false`. The design document claims 6mm OD and 2.2mm holes, but the measured evidence contradicts this.
- R6: FAIL. While a void was created (607.5 mm³), the simulation reports `opening_intersected: 0.0`. This indicates the cutout did not actually penetrate the wall to create an opening to the outside; it is likely an internal void or incorrectly positioned.
- R7: PASS. Measured mass is 65.47 g, which is $\le$ 70 g.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Floor thickness and coverage verified.
R3: PASS - Board cavity volume is 0.0.
R4: PASS - Dimensions are 85x55x31.
R5: FAIL - Probed bosses failed both outer diameter and pilot hole requirements.
R6: FAIL - Cutout did not create an opening in the wall (opening_intersected = 0.0).
R7: PASS - Mass is 65.47 g.

## Problems
- USB-C Cutout: The cutout does not penetrate the $-X$ wall to create an external opening.
- Screw Bosses: The bosses at $(\pm35, \pm20)$ do not meet the required outer diameter ($\ge$ 6 mm) or pilot hole (2.2 mm dia, $\ge$ 4 mm deep) specifications.

SIM_CODE_ISSUE: no