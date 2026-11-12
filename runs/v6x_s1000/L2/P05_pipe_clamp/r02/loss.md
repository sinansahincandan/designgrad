## Verdicts
R1: FAIL - Simulation detected 2 solids instead of 1.
R2: FAIL - Measured Y extent is 22.0 mm (design claims 20 mm).
R3: PASS - Pipe volume is free of material.
R4: PASS - Material exists in the specified band.
R5: FAIL - Screw holes at $(\pm 27, 0)$ do not intersect the solid material.
R6: FAIL - Flange region is only 60% solid.
R7: PASS - Mass is $5.27\text{ g}$.

## Problems
- R1/R5/R6: The part is not a single manifold solid; components are disconnected, causing the screw holes to miss the material and flanges to be incomplete.
- R2: Y extent is 22 mm instead of the designed 20 mm.
- R5: Screw hole locations $(\pm 27, 0)$ do not intersect the solid body.

SIM_CODE_ISSUE: no