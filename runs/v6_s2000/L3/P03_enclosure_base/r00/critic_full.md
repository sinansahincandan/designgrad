## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms floor covers the whole board area and is at least 2mm thick.
- R3: PASS. Simulation confirms the specified volume is empty.
- R4: PASS. Bounding box matches dimensions (85x55) and height (32).
- R5: FAIL. Simulation reports "Hole Not Open" for all four bosses. The visual review also notes that screw bosses are missing from the interior. Even if they exist as solids, they fail the hole requirement.
- R6: FAIL. Simulation shows 0.0 intersection/presence for the cutout and wall at that location. Visual review confirms the USB-C cutout is missing.
- R7: PASS. Mass is measured at 66.38g, which is $\le$ 70g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms floor thickness and coverage.
R3: PASS - Simulation confirms board space is empty.
R4: PASS - Bounding box matches specification.
R5: FAIL - Simulation indicates holes are not open; visual review shows bosses are missing.
R6: FAIL - Simulation and visual review confirm the cutout is missing.
R7: PASS - Measured mass 66.38g is within limit.

## Problems
- USB-C Cutout (R6): The cutout is entirely missing from the -X wall.
- Screw Bosses (R5): The bosses are missing from the interior, and even if present, the holes are not open to the top.

SIM_CODE_ISSUE: no