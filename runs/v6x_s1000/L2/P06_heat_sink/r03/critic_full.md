## Working
- R1: Evidence shows 1 solid. PASS.
- R2: BBox shows 40x40 footprint and 23mm height ($\le$ 25mm). PASS.
- R3: The design document claims a solid base from $z=0$ to $z=3$, but the simulation probe (grid-based check) failed. This indicates that the mounting holes (subtracted at $\pm15, 0$) or other features have compromised the requirement of a "solid base... over the whole footprint". Since R3 requires the base to be solid over the *whole* footprint and the holes are subtractions, the presence of holes means it is not a solid base over the whole footprint. FAIL.
- R4: Measured $R = 8.68$ K/W ($\le$ 9). PASS.
- R5: The simulation reports FAIL for both hole existence/base-presence and screwdriver access. While the design document describes $\varnothing$8mm clearance voids (radius 4mm) which should satisfy the "no material within 3mm" rule, the simulation's failure suggests the geometry was not implemented as described or the holes were not correctly placed/subtracted. FAIL.
- R6: Measured mass is 31.77g ($\le$ 45g). PASS.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - BBox is 40x40x23 mm.
R3: FAIL - Simulation probe failed; mounting holes subtract from the base, meaning it is not a solid base over the whole footprint.
R4: PASS - Measured R = 8.68 K/W.
R5: FAIL - Simulation reports failure for hole existence and screwdriver access.
R6: PASS - Measured mass is 31.77 g.

## Problems
- Mounting Holes (R5): The simulation failed to verify the presence of holes and the required clearance for screwdriver access despite the design intent.
- Base Integrity (R3): The mounting holes violate the requirement for a solid base over the whole footprint.

SIM_CODE_ISSUE: no