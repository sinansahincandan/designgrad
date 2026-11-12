## Verdicts
R1: FAIL - Simulation detected 5 solids instead of 1.
R2: FAIL - Zmin is -15.5 mm; does not sit on z = 0.
R3: PASS - Pipe volume is free of material.
R4: FAIL - Material coverage in the band |x| <= 7, r in [12.7, 15.5] is only 0.5333.
R5: FAIL - Screw holes are not correctly implemented as voids at (+-27, 0).
R6: FAIL - Flange region density is 0.09; flanges are not solid from z=0 to 3.
R7: PASS - Mass is 10.161 g.

## Problems
- Connectivity: The design consists of 5 separate solids instead of one single valid solid (R1).
- Z-Positioning: The part extends to z = -15.5 mm; it must sit on z = 0 (R2).
- Flange Geometry: Flanges are not solid in the required region |x| in [18.5, 23], |y| <= 4, z in [0, 3] (R6).
- Band Coverage: Material is missing from parts of the band between 12.7 and 15.5 mm from the axis (R4).
- Screw Holes: The holes at (+-27, 0) are not correctly subtracted as vertical voids through the flanges (R5).

SIM_CODE_ISSUE: no