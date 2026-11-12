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