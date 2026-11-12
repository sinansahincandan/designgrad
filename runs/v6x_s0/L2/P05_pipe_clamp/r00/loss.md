## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Y extent is 31.0 mm (limit 18-22) and Zmin is -17.5 (must be 0).
R3: FAIL - Non-zero intersection volume with pipe axis cylinder.
R4: FAIL - Insufficient material in the specified band above the pipe.
R5: FAIL - Holes at (+-27, 0) are not correctly formed/empty.
R6: PASS - Flange geometry meets thickness and position requirements.
R7: FAIL - Mass is 39.54 g (limit 25 g).

## Problems
- Mass: Measured 39.54 g, must be <= 25 g.
- Clamp Width: Y extent is 31.0 mm, must be between 18 and 22 mm.
- Pipe Clearance: Material exists in the pipe volume (R3), must be free.
- Saddle Coverage: Insufficient material in the band 12.7 to 15.5 mm from axis (R4).
- Mounting: Zmin is -17.5 mm, must sit on z = 0.
- Screw Holes: Holes at (+-27, 0) are not correctly implemented/empty.

SIM_CODE_ISSUE: no