## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box $y$ range is $[0, 30]$, which violates $-20 \le y \le 20$. The $x$ max is 150, but the envelope check shows it fits within the limits; however, the $y$ offset is a failure.
- R3: FAIL. Simulation reports diameter/access failure. Render evidence shows holes are oriented along Z instead of X and are centered at $y=1.75$ instead of $y=0$. Screw heights are $z=35, 75$ instead of $20, 60$.
- R4: FAIL. Simulation shows material exists above $z=110$ for $x \ge 8$. Also, support column fill at $x[140, 150]$ is insufficient (value 0.054).
- R5: PASS. $\sigma = 0.378 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. $\delta = 0.012 \text{ mm} \le 2.0 \text{ mm}$.
- R7: FAIL. Measured mass is $119.34\text{g}$, which exceeds the limit of $90\text{g}$.

## Verdicts
R1: PASS - 1 solid detected.
R2: FAIL - y-range [0, 30] violates [-20, 20].
R3: FAIL - Holes are oriented along Z instead of X; centers at (y=1.75, z=35/75) violate (y=0, z=20/60).
R4: FAIL - Material exists above z=110 for x>=8 and insufficient support at x[140, 150].
R5: PASS - Stress 0.378 MPa <= 20 MPa.
R6: PASS - Deflection 0.012 mm <= 2.0 mm.
R7: FAIL - Mass 119.34g exceeds 90g limit.

## Problems
- Screw Holes: Axis is along Z, should be along X; centers are at (y=1.75, z=35) and (y=1.75, z=75), should be (y=0, z=20) and (y=0, z=60).
- Mass: 119.34g exceeds 90g limit.
- Envelope: y-range is [0, 30], should be within [-20, 20].
- Shelf Support: Material exists above z=110 for x>=8; support at x[140, 150] is insufficient.

SIM_CODE_ISSUE: no