## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Floor thickness and coverage verified by intersection test.
- R3: PASS. Intersection test shows zero material in the specified board cavity volume.
- R4: PASS. Bounding box dimensions (85x55) and height (32) meet requirements.
- R5: FAIL. The simulation probe failed. While the design document claims bosses span $z=2$ to $z=8$, the requirement specifies the pilot hole must be "open at its top". If the boss ends at $z=8$ (the bottom of the board cavity), and the hole is contained within that boss, it cannot be "open" to the board unless the hole extends into the $z > 8$ region or the boss height is adjusted. More critically, the simulation probe failed on this requirement.
- R6: FAIL. The simulation reports `empty_ratio: 0.0` for the cutout void, meaning no material was actually removed to create the opening. This is corroborated by the visual reviewer who noted the cutout is not visible on the -X wall.
- R7: PASS. Mass is ~37.35g, which is $\le$ 70g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Intersection test confirms floor coverage and thickness.
R3: PASS - Intersection test confirms cavity is empty.
R4: PASS - Bounding box matches required dimensions.
R5: FAIL - Simulation probe failed; pilot hole functionality/geometry is incorrect.
R6: FAIL - Simulation shows 0.0 volume removed for the cutout; visual inspection confirms no opening exists.
R7: PASS - Mass (37.35g) is below 70g limit.

## Problems
- USB-C Cutout: The cutout has 0mm width/height in the final part (empty_ratio 0.0); it must be at least 9mm (Y) and 3mm (Z).
- Screw Bosses: Pilot holes are not correctly implemented or open to the board; simulation probe failed.

SIM_CODE_ISSUE: no