## Working
- R1: The simulation counted 2 solids in the STEP file. Requirement requires one single solid. FAIL.
- R2: BBox shows X=54, Y=22, Zmin $\approx$ 0. While X is within limits ($\le 80$), Y is exactly at the upper limit (22). However, the simulation reports a failure for R2 despite values appearing to meet thresholds; looking closer at the evidence `value=[54.0, 22.0, -0.0]`, it seems the check failed on precision or specific bounds. Regardless, the design claims Y extent is 20mm ($y \in [-10, 10]$), but the simulation measures 22.0. FAIL.
- R3: Intersection volume ratio with pipe radius is near zero. PASS.
- R4: Sampling confirms material exists in the specified radial band for $|x| \le 7$. PASS.
- R5: Cylinder intersection check at $(\pm 27, 0)$ returned values $[[0.0, 0.03], [0.03, 0.03]]$, which are near zero. This implies the screw holes (voids) do not actually intersect the solid material at those coordinates. FAIL.
- R6: Sampling in the flange region $|x| \in [18.5, 23], |y| \le 4, z \in [0, 3]$ returned $0.6$, meaning only 60% of the required volume is solid. Requirement requires it to be solid (1.0). FAIL.
- R7: Mass calculated as $5.27\text{ g}$, which is $\le 25\text{ g}$. PASS.

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