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