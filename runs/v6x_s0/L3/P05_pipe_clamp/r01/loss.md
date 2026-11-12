## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Y extent is 31.0 mm (required 18-22 mm).
R3: FAIL - Material exists in the pipe volume (intersection > 0).
R4: FAIL - Insufficient material in the specified band above the pipe.
R5: FAIL - Screw holes are not present/empty.
R6: PASS - Flange geometry meets requirements.
R7: PASS - Mass is ~12.46 g (required <= 25 g).

## Problems
- R2: Clamp width (Y extent) is 31.0 mm; should be between 18 and 22 mm.
- R5: Screw holes are missing/not drilled through the base.
- R3: Pipe volume contains material; must be subtracted.
- R4: Material in the band 12.7 to 15.5 mm above pipe is insufficient.

SIM_CODE_ISSUE: no