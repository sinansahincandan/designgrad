## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. BBox [0, 149] x [-7.5, 7.5] x [0, 110] is within limits.
- R3: FAIL. The simulation reports a value of 0.0 for the screw hole requirement. The visual evidence shows holes are not centered at $y=0$ (one center is at $y=6.45$). This violates the centering requirement and likely the clearance requirement.
- R4: FAIL. Simulation states "Surface at z=110: False". While the design document claims a top surface at exactly $z=110$, the measured evidence shows the part does not meet this geometric constraint.
- R5: PASS. Measured $\sigma = 0.71 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. Measured $\delta = 0.02 \text{ mm} \le 2.0 \text{ mm}$.
- R7: PASS. Measured mass $48.6 \text{ g} \le 90 \text{ g}$.

## Verdicts
R1: PASS - Simulation confirms one solid.
R2: PASS - BBox is within specified limits.
R3: FAIL - Holes are not centered at y=0 per visual evidence and simulation failed.
R4: FAIL - Measured surface is not at z=110.
R5: PASS - Measured stress 0.71 MPa <= 20 MPa.
R6: PASS - Measured deflection 0.02 mm <= 2.0 mm.
R7: PASS - Measured mass 48.6 g <= 90 g.

## Problems
- R4: Top surface height is not at $z=110$.
- R3: Screw hole centers are offset from $y=0$ (one center measured at $y=6.45$).

SIM_CODE_ISSUE: no