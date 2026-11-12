## Working
- R1: The simulation reports 2 solids in the STEP file. Requirement requires one single valid solid. FAIL.
- R2: X extent is 60 mm (<= 80), Y extent is ~20 mm (between 18 and 22). However, Zmin is -37.5, meaning it does not sit on z=0. FAIL.
- R3: The intersection volume of the pipe cylinder and the part is non-zero (0.028...). Requirement requires pipe volume to be free of material. FAIL.
- R4: The intersection volume with the specified band is 0.0. This means no material exists in the required radial band [12.7, 15.5] for |x| <= 7. FAIL.
- R5: Simulation shows holes are not empty or do not have surrounding material at (+-27, 0). FAIL.
- R6: The intersection volume of the probe boxes matches the requirement. PASS.
- R7: Mass is ~21.1 g (<= 25 g). PASS.

## Verdicts
R1: FAIL - Simulation detected 2 solids instead of 1.
R2: FAIL - Zmin is -37.5, so it does not sit on z=0.
R3: FAIL - Non-zero intersection volume (0.028) found within the pipe radius.
R4: FAIL - Zero material volume found in the required band [12.7, 15.5].
R5: FAIL - Screw holes at (+-27, 0) are not correctly implemented/empty.
R6: PASS - Flanges meet thickness and location requirements.
R7: PASS - Mass is ~21.1 g, which is <= 25 g.

## Problems
- R4: Saddle arch material; intersection volume with band [12.7, 15.5] is 0.0 mm3 instead of > 0.
- R3: Pipe clearance; non-zero intersection volume (0.028) found within the pipe radius.
- R2: Mounting surface; Zmin is -37.5 instead of 0.
- R1: Topology; design contains 2 solids instead of 1.
- R5: Screw holes; holes at (+-27, 0) are not correctly formed/empty.

SIM_CODE_ISSUE: no