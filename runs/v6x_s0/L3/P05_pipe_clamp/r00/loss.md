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