## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. BBox shows Y=40 mm, which exceeds the limit of 18-22 mm. Zmin is -3.0, meaning it does not sit on z=0 (it is centered or offset incorrectly). X extent (54) is fine.
- R3: PASS. Intersection volume with pipe radius is 0.
- R4: PASS. Sampling confirms material in the required band.
- R5: FAIL. Simulation shows cylinder intersection at (+-27, 0) is nearly zero ([0.03, 0.03]), meaning the holes were not successfully subtracted or are missing. This matches the visual reviewer report.
- R6: FAIL. Sampling in flange region is only 0.6 (60%), meaning the flanges do not provide full coverage of the required volume.
- R7: PASS. Mass is 14.63 g, which is <= 25 g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Y extent is 40 mm (limit 18-22) and Zmin is -3 (must be 0).
R3: PASS - Pipe volume is free of material.
R4: PASS - Material exists in the required band.
R5: FAIL - Holes are missing/not subtracted at (+-27, 0).
R6: FAIL - Flange region coverage is only 60%.
R7: PASS - Mass is 14.63 g.

## Problems
- Clamp Width (R2): Y extent is 40 mm; should be between 18 and 22 mm.
- Mounting Surface (R2): Zmin is -3.0 mm; must sit on z = 0.
- Screw Holes (R5): Holes are missing at (+-27, 0).
- Flange Coverage (R6): Material coverage in flange region is 60%; must be 100%.

SIM_CODE_ISSUE: no