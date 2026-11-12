## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Bounding box [0, 150.5] x [-20, 20] x [0, 117.39] is within limits.
- R3: FAIL. Simulation reports "walled" status for holes (presence of material where it should be empty/clear).
- R4: FAIL. Simulation reports `above_z110: true`. Bounding box shows $z_{max} = 117.39$, violating the requirement that nothing may be above $z=110$ for $x \ge 8$.
- R5: PASS. Measured stress $\sigma \approx 0.26 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. Measured deflection $\delta \approx 0.009 \text{ mm} \le 2.0 \text{ mm}$.
- R7: FAIL. Measured mass is $151.49 \text{ g}$, which exceeds the limit of $90 \text{ g}$.

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