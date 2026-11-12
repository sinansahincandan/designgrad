## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured Y extent is 31.0 mm, which exceeds the required range of 18 to 22 mm. X extent (54 mm) is within limits.
- R3: FAIL. Intersection volume with the pipe cylinder is non-zero (0.117), meaning material exists where it should be free.
- R4: FAIL. Measured intersection volume in the specified band/region is only ~24.8% of the target shell, meaning the clamp does not sufficiently wrap over the top.
- R5: FAIL. Simulation shows holes are not empty (false), and visual evidence confirms screw holes are missing from the part.
- R6: PASS. Measured intersection with probe box is 100%, so flanges meet thickness and location requirements.
- R7: PASS. Mass is ~12.46 g, which is <= 25 g.

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