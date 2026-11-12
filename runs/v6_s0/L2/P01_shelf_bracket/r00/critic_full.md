## Working
- R1: PASS. Evidence shows 1 solid.
- R2: FAIL. Bounding box $y$ range is $[0, 30]$. Requirement is $[-20, 20]$. The part is off-center on the Y axis. Also, max $x$ is 150, which fits, but the Y violation is sufficient for failure.
- R3: FAIL. Simulation reports `diameter_check_passed: false`. Even though the design mentions clearance cutouts, the measured evidence indicates the screw hole requirements (diameter or screwdriver access) were not met.
- R4: FAIL. Simulation shows material exists above $z=110$ for $x \ge 8$. The requirement states "Nothing of the bracket may be above z = 110 for x >= 8".
- R5: PASS. Measured stress $\approx 0.38 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. Measured deflection $\approx 0.013 \text{ mm} \le 2.0 \text{ mm}$.
- R7: FAIL. Measured mass is $119.34\text{ g}$, which exceeds the limit of $90\text{ g}$.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Y range [0, 30] exceeds [-20, 20].
R3: FAIL - Screw hole diameter or screwdriver access check failed.
R4: FAIL - Material detected above z=110 for x >= 8.
R5: PASS - Stress 0.378 MPa <= 20 MPa.
R6: PASS - Deflection 0.013 mm <= 2.0 mm.
R7: FAIL - Mass 119.34 g exceeds 90 g.

## Problems
- Mass: Current mass is 119.34 g, must be <= 90 g.
- Y-Envelope: Y range is [0, 30], must be within [-20, 20].
- Z-Clearance: Material exists above z=110 for x >= 8, must have no material above z=110 for x >= 8.
- Screw Holes: Diameter or screwdriver access clearance failed.

SIM_CODE_ISSUE: no