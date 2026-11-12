## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Floor thickness is 8 mm ($z=0$ to $z=8$), which meets the $\ge 2$ mm requirement.
- R3: PASS. Simulation confirms zero intersection with the specified void region.
- R4: PASS. Bounding box dimensions are 85 x 55 x 32 mm, matching requirements.
- R5: FAIL. The simulation probe for all four bosses returned `false` for OD, hole, and wall checks. While the design document claims $\varnothing 7$ mm bosses with $\varnothing 2.2$ mm holes at $(\pm 35, \pm 20)$, the measured evidence shows these features do not exist or are not correctly formed in the geometry at those coordinates.
- R6: PASS. Cutout is present and meets dimensions.
- R7: PASS. Mass is 66.38 g, which is $\le 70$ g.

## Verdicts
R1: PASS - Evidence from simulation (value=1).
R2: PASS - Evidence from simulation (filled fraction 1.0 in floor probe box).
R3: PASS - Evidence from simulation (empty fraction 0.0 in void probe box).
R4: PASS - Evidence from simulation (bounding box 85x55x32).
R5: FAIL - Evidence from simulation (probed locations at $(\pm 35, \pm 20)$ returned false for all boss parameters).
R6: PASS - Evidence from simulation (cutout void confirmed).
R7: PASS - Evidence from simulation (mass = 66.38 g).

## Problems
Screw Bosses: The bosses at $(\pm 35, \pm 20)$ are missing or incorrectly modeled; the simulation probe failed to detect the diameter, hole, or wall thickness at these locations.

SIM_CODE_ISSUE: no