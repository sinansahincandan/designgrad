## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Bounding box [0, 160] x [-15, 19] x [0, 110] is within limits.
- R3: FAIL. Simulation shows diameter check failed. Reviewer notes confirm screw hole axes are at $x=83.57$ instead of the wall ($x \approx 0$), meaning they do not sit on the wall as required.
- R4: FAIL. Simulation reports a value of 0.81 for support column fill (likely indicating failure to meet the "solid material" requirement) and reviewer notes confirm the pillar is missing or incorrectly placed between $x=140$ and $x=150$.
- R5: PASS. $\sigma = 21000 \cdot 55.01 / 2194314.85 \approx 0.53$ MPa, which is $\le 20$ MPa.
- R6: PASS. $\delta \approx 0.018$ mm, which is $\le 2.0$ mm.
- R7: FAIL. Measured mass is $188.06$ g, which exceeds the limit of $90$ g.

## Verdicts
R1: PASS
R2: PASS
R3: FAIL - Screw hole axes are at x=83.57 instead of being centered on the wall (x near 0).
R4: FAIL - No solid material exists directly below z=110 between x=140 and x=150 around y=0.
R5: PASS
R6: PASS
R7: FAIL - Mass is 188.06 g, exceeding the limit of 90 g.

## Problems
- Mass: Current mass is 188.06 g; must be $\le$ 90 g.
- Screw Holes: Axes are at x=83.57; must be centered on the wall (x near 0).
- Shelf Support: Material missing between x=140 and x=150 under z=110; must have solid material there.

SIM_CODE_ISSUE: no