## Working
- R1: FAIL. Simulation reports 2 solids. Reviewer confirms upper band and base are disconnected.
- R2: FAIL. BBox Y is 43.5 mm (required 18-22 mm). Zmin is -15.5 (required z=0). X extent is 60 mm (PASS, <= 80).
- R3: FAIL. Intersection volume ratio is 0.0484, meaning material exists inside the pipe radius. Reviewer notes axis is incorrectly placed near z=0 instead of z=12.5.
- R4: PASS. Measured via point sampling.
- R5: FAIL. Simulation shows holes are not at x = +-27 (values [0.0, 0.025] suggest they are near the origin). Reviewer confirms they are near x = +-10.
- R6: FAIL. Sampling in flange region returns 0.0 volume. Reviewer notes part extends to z = -15.5 instead of sitting on z=0.
- R7: PASS. Mass is 18.813 g (<= 25 g).

## Verdicts
R1: FAIL - Simulation reports 2 solids; parts are disconnected.
R2: FAIL - Y extent is 43.5 mm (required 18-22 mm) and Zmin is -15.5 (required z=0).
R3: FAIL - Material exists within the pipe radius; axis is incorrectly positioned.
R4: PASS - Measured via point sampling.
R5: FAIL - Holes are not centered at x = +-27.
R6: FAIL - No solid material found in specified flange region.
R7: PASS - Mass is 18.813 g.

## Problems
- R2/R6: Base position; Zmin is -15.5 mm, should be 0 mm.
- R2: Clamp width; Y extent is 43.5 mm, should be between 18 and 22 mm.
- R3: Pipe axis; z-coordinate of cutout is near 0, should be 12.5 mm.
- R5: Screw hole position; x-coordinates are approx +-10 mm, should be +-27 mm.
- R1: Connectivity; upper band and base are disconnected solids.

SIM_CODE_ISSUE: no