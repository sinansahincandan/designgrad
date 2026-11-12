## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. BBox shows Y=31.0 mm, which exceeds the limit of 18-22 mm. Zmin is -17.5 mm, meaning it does not sit on z=0 (it penetrates below). X extent is 64.0 mm (<= 80), so that part is fine.
- R3: FAIL. Intersection volume with the pipe cylinder is non-zero (0.278...), meaning material exists where the pipe should be free.
- R4: FAIL. The intersection volume with the required band is only ~27% of the shell volume, meaning the clamp does not sufficiently wrap over the top as specified.
- R5: FAIL. Simulation shows holes are not empty/correctly placed at (+-27, 0).
- R6: PASS. Probe box intersection confirms flange geometry is correct.
- R7: FAIL. Mass is measured at ~39.54 g, which exceeds the limit of 25 g. (Note: The design doc claimed ~1.98g, but simulation evidence is the source of truth).

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