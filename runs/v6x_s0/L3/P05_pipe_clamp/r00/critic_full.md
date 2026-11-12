## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured Y extent is 31 mm (spec: 18-22 mm). Measured X extent is 64 mm (spec: <= 80 mm, this part is okay). However, Zmin is -17.5 (spec: must sit on z=0).
- R3: FAIL. Intersection volume with the pipe cylinder is non-zero (0.278), meaning material exists where the pipe should be.
- R4: FAIL. Intersection volume with the required band is 0.276, meaning the required material in that specific shell/region is missing.
- R5: FAIL. Simulation shows holes are not empty/correctly placed at (+-27, 0). Reviewer notes they are located too high up.
- R6: PASS. Intersection volume with probe boxes for flanges is correct.
- R7: FAIL. Measured mass is 39.54 g (spec: <= 25 g).

## Verdicts
R1: PASS - Counted 1 solid.
R2: FAIL - Y extent is 31 mm (req: 18-22 mm) and Zmin is -17.5 (req: z=0).
R3: FAIL - Non-zero intersection volume with pipe axis cylinder.
R4: FAIL - Intersection volume with required band is incorrect/missing material.
R5: FAIL - Holes are not located at (+-27, 0) through surface flanges.
R6: PASS - Flange thickness and position requirements met.
R7: FAIL - Mass is 39.54 g (req: <= 25 g).

## Problems
- Geometry/Form: The part is a large cylinder instead of a saddle clamp, causing R3, R4, and R7 failures.
- Z-Position: Part extends to z = -17.5; must sit on z = 0.
- Width (Y): Y extent is 31 mm; must be between 18 and 22 mm.
- Screw Holes: Holes are not at (x, y) = (+-27, 0); they are located too high.
- Mass: Mass is 39.54 g; must be <= 25 g.

SIM_CODE_ISSUE: no