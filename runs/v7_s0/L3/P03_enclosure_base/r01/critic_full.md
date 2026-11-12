## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms floor exists from z=0 to 2 under board area.
- R3: PASS. Simulation confirms the specified volume is empty.
- R4: PASS. Bounding box shows dimensions 85x55 and height 31 (within 30-32.5 range).
- R5: FAIL. The design document claims bosses exist, but the visual reviewer notes they are not visible as distinct features. While simulation says "All bosses checked" with holes present, the visual evidence suggests the boss material itself is missing or incorrectly modeled (the 'cylindrical_faces' data shows only the hole). If the boss material is gone, it fails R5.
- R6: FAIL. Simulation reports `empty_ratio: 0.0` for the cutout void, meaning no volume was removed. The visual reviewer confirms the cutout is missing from the -X wall.
- R7: PASS. Mass is ~65.47g, which is $\le$ 70g.

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