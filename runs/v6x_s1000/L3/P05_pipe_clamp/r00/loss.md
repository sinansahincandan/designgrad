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