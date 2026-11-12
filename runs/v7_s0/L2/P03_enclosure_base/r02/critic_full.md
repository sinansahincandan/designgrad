## Working
- R1: Evidence shows 1 solid. PASS.
- R2: Intersected floor box (80x50x2 at z=0) with part; ratio=1.0. PASS.
- R3: The requirement states the region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be completely free of material. Simulation shows an intersection ratio of 0.1667 (meaning ~83% of that volume is occupied by material). FAIL.
- R4: Bounding box measured at 85x55 and zmax=31. This meets the dimensions and height requirements. PASS.
- R5: Bosses checked at coordinates, OD/hole diameter/depth verified. PASS.
- R6: Cutout void and wall material volume verified. PASS.
- R7: Measured mass is 85.39 g. Requirement is <= 70 g. FAIL.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Floor coverage ratio is 1.0.
R3: FAIL - Intersection ratio of 0.1667 indicates material exists in the specified board space.
R4: PASS - Dimensions are 85x55x31.
R5: PASS - Bosses meet diameter and hole depth requirements.
R6: PASS - Cutout verified.
R7: FAIL - Mass is 85.39 g, exceeding the 70 g limit.

## Problems
- Board Space (R3): The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 contains material; it must be completely free.
- Mass (R7): Current mass is 85.39 g; must be <= 70 g.

SIM_CODE_ISSUE: no