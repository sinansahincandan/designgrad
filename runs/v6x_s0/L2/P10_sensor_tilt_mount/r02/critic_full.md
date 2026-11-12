## Working
- R1: Evidence shows 1 solid. PASS.
- R2: $z_{min}$ is -18.3, not $\ge 0$. Screw holes at $(\pm 20, -10)$ were not found/probed correctly (value [-18.3, [0,0]]). FAIL.
- R3: Area 2157.54 mm² $\ge$ 900 mm². Normal is correct. PASS.
- R4: Face center height $z = 12.05$, which is outside the required range [35, 50]. FAIL.
- R5: Probing for sensor holes at face center $\pm 10$ mm along X failed to find them. FAIL.
- R6: Combined CoM margin check passed (margin $\ge 5$ mm). PASS.
- R7: Mass is 42.12 g, which exceeds the limit of 35 g. FAIL.

## Verdicts
R1: PASS - Found 1 solid.
R2: FAIL - $z_{min}$ is -18.3 instead of $\ge 0$.
R3: PASS - Area 2157.54 mm² and normal are correct.
R4: FAIL - Face center height is 12.05 mm, not between 35 and 50 mm.
R5: FAIL - Sensor holes were not detected at the specified locations.
R6: PASS - Combined CoM margin $\ge 5$ mm.
R7: FAIL - Mass is 42.12 g, exceeding 35 g limit.

## Problems
- Mass: Current mass 42.12 g exceeds maximum 35 g.
- Face Height: Center height 12.05 mm is below required 35–50 mm range.
- Base Placement: $z_{min}$ is -18.3 mm instead of $\ge 0$.
- Sensor Holes: Holes not found at face center $\pm 10$ mm along X.
- Base Screw Holes: Holes not found at $(\pm 20, -10)$.

SIM_CODE_ISSUE: no