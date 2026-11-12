## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness and coverage.
R3: PASS - Simulation confirms board space is void.
R4: PASS - Bounding box matches required dimensions and height.
R5: FAIL - Visual evidence shows bosses are not distinct features/material is missing despite holes being present.
R6: FAIL - Simulation shows 0% empty ratio in cutout region; visual reviewer confirms cutout is missing.
R7: PASS - Measured mass 65.47g is $\le$ 70g.

## Problems
- USB-C Cutout (R6): The opening is missing from the -X wall; it should be a 9mm (Y) x 3mm (Z) void.
- Screw Bosses (R5): The boss material is missing or not visible as distinct features; they must be solid round bosses (OD $\ge$ 6mm) from floor to z=8.

SIM_CODE_ISSUE: no