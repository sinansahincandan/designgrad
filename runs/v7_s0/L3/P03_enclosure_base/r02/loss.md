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