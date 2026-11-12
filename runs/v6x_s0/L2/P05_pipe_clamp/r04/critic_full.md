## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. BBox shows Y extent is 34.0 mm, which exceeds the required range of 18 to 22 mm. Zmin is -7.5, meaning it does not sit on z=0 (it penetrates below it). X extent is 60.0, which is <= 80.
- R3: FAIL. Intersection volume with the pipe radius is non-zero (0.14), meaning material exists where the pipe should be free.
- R4: FAIL. The intersection volume of the specified band and the part is only ~25% of the required shell volume, meaning the arch does not sufficiently cover the band.
- R5: FAIL. Simulation shows holes are not "empty" or do not meet the criteria (likely due to geometry/alignment issues).
- R6: PASS. Probe box intersection confirms flange thickness and position.
- R7: PASS. Mass is 22.75 g, which is <= 25 g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Y extent is 34.0 mm (required 18-22) and Zmin is -7.5 (required 0).
R3: FAIL - Non-zero intersection volume with pipe radius detected.
R4: FAIL - Insufficient material in the specified radial band.
R5: FAIL - Screw holes failed emptiness/material check.
R6: PASS - Flange geometry meets thickness and position requirements.
R7: PASS - Mass is 22.75 g (required <= 25 g).

## Problems
- Clamp Width: Y extent is 34.0 mm; should be between 18 and 22 mm.
- Mounting Surface: Zmin is -7.5; must sit on z = 0.
- Pipe Clearance: Material exists within the pipe radius (r=12.6); must be free of material.
- Saddle Coverage: Arch does not sufficiently fill the band 12.7 to 15.5 mm from axis; coverage is ~25%.
- Screw Holes: Holes at (+-27, 0) failed verification.

SIM_CODE_ISSUE: no