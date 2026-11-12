## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box shows $y \in [-60, 20]$. Requirement is $-20 \le y \le 20$. The part is too wide in the Y direction.
- R3: PASS. Simulation confirms diameter and screwdriver clearance (no material within 4mm for $x \ge 10$).
- R4: FAIL. Simulation reports failure on support column fill at $x[140, 150]$ and excess volume above $z=110$ for $x \ge 8$.
- R5: PASS. Measured stress $\approx 0.275\text{ MPa} \le 20\text{ MPa}$.
- R6: PASS. Measured deflection $\approx 0.009\text{ mm} \le 2.0\text{ mm}$.
- R7: FAIL. Measured mass is $534.08\text{ g}$, which exceeds the limit of $90\text{ g}$ by a factor of nearly 6.

## Verdicts
R1: PASS - Simulation confirms one solid.
R2: FAIL - Y dimension is [-60, 20], exceeding requirement [-20, 20].
R3: PASS - Diameter and clearance requirements met per simulation.
R4: FAIL - Simulation indicates failure in support column fill and/or height constraints.
R5: PASS - Measured stress 0.275 MPa is $\le$ 20 MPa.
R6: PASS - Measured deflection 0.009 mm is $\le$ 2.0 mm.
R7: FAIL - Measured mass 534.08 g exceeds limit of 90 g.

## Problems
- Mass: Current mass is 534.08 g; must be $\le$ 90 g.
- Envelope (Y): Y range is [-60, 20]; must be within [-20, 20].
- Shelf Support/Height: Fails R4 constraints regarding material at $x \in [140, 150]$ and height for $x \ge 8$.

SIM_CODE_ISSUE: no