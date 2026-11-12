## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Simulation indicates material presence ("walled") in screw hole clearance zones.
R4: FAIL - Part extends to $z=117.39$, violating the $z \le 110$ limit for $x \ge 8$.
R5: PASS - Stress is $0.26 \text{ MPa} \le 20 \text{ MPa}$.
R6: PASS - Deflection is $0.009 \text{ mm} \le 2.0 \text{ mm}$.
R7: FAIL - Mass is $151.49 \text{ g} > 90 \text{ g}$.

## Problems
- Mass: Current mass is $151.49 \text{ g}$, must be $\le 90 \text{ g}$.
- Geometry Constraint: Part height reaches $z=117.39$, must be $\le 110$ for $x \ge 8$.
- Screw Hole Clearance: Material exists within the required 4mm clearance zone around hole axes.

SIM_CODE_ISSUE: no