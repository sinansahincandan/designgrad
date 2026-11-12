## Working
- R1: The simulation counted 2 solids in the STEP file, whereas the requirement specifies one single valid solid. FAIL.
- R2: Measured bounding box shows $x_{ext} \approx 155.6$ mm (limit 100), $z_{ext} \approx 156.5$ mm (limit 120), and $z_{min} \approx -45.1$ mm (must be $\ge 0$). FAIL.
- R3: Point-in-mesh sampling detected 238 points of the phone volume intersecting the stand. FAIL.
- R4: Volumetric sampling confirms material exists in the specified region ($a \in [90, 110], b \in [-2, 0]$). PASS.
- R5: Volumetric sampling confirms material exists in the seat and lip regions. PASS.
- R6: Combined COM is at $x = -17.48$. The footprint x-range is $[-77.79, 77.79]$. The margin to the edge is $77.79 - |-17.48| = 60.31$ mm, which is $> 5$ mm. PASS.
- R7: Measured mass is $\approx 200.36$ g (limit 60 g). FAIL.

## Verdicts
R1: FAIL - Counted 2 solids in STEP file.
R2: FAIL - x_ext=155.57, z_ext=156.49, and z_min=-45.14 exceed limits.
R3: FAIL - 238 intersection points detected.
R4: PASS - Material found in specified region.
R5: PASS - Material found in seat and lip regions.
R6: PASS - Combined COM projects within footprint with $>5$mm margin.
R7: FAIL - Mass is 200.36 g (limit 60 g).

## Problems
- R1: The design consists of 2 separate solids instead of one single solid.
- R2: Footprint x_ext=155.57 mm (>100), height z_ext=156.49 mm (>120), and z_min=-45.14 mm (<0).
- R3: Stand intersects phone volume at 238 points.
- R7: Mass is 200.36 g instead of $\le 60$ g.

SIM_CODE_ISSUE: no