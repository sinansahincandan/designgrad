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