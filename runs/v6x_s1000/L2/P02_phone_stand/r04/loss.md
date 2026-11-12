## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Extents (x=160, z=200) exceed limits (x<=100, z<=120).
R3: FAIL - 1470 intersection points detected within phone volume.
R4: PASS - Material confirmed in specified back support region.
R5: PASS - Material confirmed in seat and lip regions.
R6: PASS - Combined COM projects inside footprint with >5mm margin.
R7: FAIL - Mass is 922.56 g, exceeding the 60 g limit.

## Problems
- Mass: Current mass is 922.56 g; must be <= 60 g.
- Footprint/Height: X extent is 160 mm (limit 100) and Z height is 200 mm (limit 120).
- Intersection: Stand intersects phone volume at 1470 points.

SIM_CODE_ISSUE: no