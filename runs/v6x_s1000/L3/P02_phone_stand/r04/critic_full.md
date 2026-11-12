## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured x-extent is 182.95 mm (limit 100), z-height is 158.17 mm (limit 120), and min z is -20.0 (must be $\ge$ 0).
- R3: FAIL. Simulation detected 1134 intersection points within the phone volume.
- R4: PASS. Material found in specified region $a \in [90, 110], b \in [-2, 0]$.
- R5: PASS. Material found in seat and lip regions.
- R6: PASS. Combined COM projects at $x = -25.94$, which is within the footprint $x \in [-112.9, 70.0]$ with a margin $> 5\text{ mm}$.
- R7: FAIL. Measured mass is 363.51 g (limit 60 g).

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - x-extent 182.95 > 100, height 158.17 > 120, min z = -20 < 0.
R3: FAIL - 1134 intersection points detected.
R4: PASS - Material confirmed in specified region.
R5: PASS - Material confirmed in seat and lip regions.
R6: PASS - Combined COM projects inside footprint with sufficient margin.
R7: FAIL - Mass 363.51 g > 60 g.

## Problems
- Mass/Volume: Mass is 363.51 g; should be $\le$ 60 g.
- Footprint/Height: x-extent is 182.95 mm (limit 100), height is 158.17 mm (limit 120).
- Z-Position: Min z is -20.0; should be $\ge$ 0.
- Intersection: 1134 points of intersection with phone volume detected.

SIM_CODE_ISSUE: no