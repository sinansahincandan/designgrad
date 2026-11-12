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