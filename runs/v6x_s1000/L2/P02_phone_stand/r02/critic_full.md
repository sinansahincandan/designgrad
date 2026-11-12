## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured x-extent is ~158.5 mm and z-height is ~159.9 mm. Specification requires x $\le$ 100 mm and height $\le$ 120 mm.
- R3: FAIL. Simulation found 1197 intersection points within the phone volume.
- R4: PASS. Material verified in the specified $a, b, y$ range.
- R5: PASS. Seat and lip material presence verified in required ranges.
- R6: PASS. Combined COM (8.38, 1.05) is within footprint x[-68.5, 90.0], y[-40, 40] with sufficient margin.
- R7: FAIL. Measured mass is ~925.4 g. Specification requires $\le$ 60 g. The volume (746316 mm³) is massive compared to the design claim (~32000 mm³), indicating a significant scaling or modeling error.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - x-extent 158.5 mm > 100 mm, height 159.9 mm > 120 mm.
R3: FAIL - 1197 intersection points detected.
R4: PASS - Material verified in $a \in [90, 110], b \in [-2, 0], |y| \le 15$.
R5: PASS - Seat and lip material presence verified.
R6: PASS - COM projects within footprint with margin.
R7: FAIL - Mass 925.4 g > 60 g.

## Problems
- Mass/Volume: Measured mass is 925.4 g; must be $\le$ 60 g.
- Dimensions: x-extent is 158.5 mm (max 100 mm) and height is 159.9 mm (max 120 mm).
- Intersection: Stand intersects phone volume at 1197 points.

SIM_CODE_ISSUE: yes