## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box $y$ range is $[-25, 25]$, which exceeds the required $[-20, 20]$.
- R3: FAIL. The simulation check for diameter and clearance failed (diameter_check_ok: false). While the design claims to provide access channels, the measured evidence indicates the holes do not meet the specification requirements.
- R4: PASS. Top surface is at $z=110$, material exists in the required range, and nothing is above $z=110$ for $x \ge 8$.
- R5: PASS. Measured stress $\sigma = 2.535$ MPa is $\le 20$ MPa.
- R6: PASS. Measured deflection $\delta = 0.274$ mm is $\le 2.0$ mm.
- R7: FAIL. Measured mass is $228.16$ g, which exceeds the limit of $90$ g.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - y range is [-25, 25], must be within [-20, 20].
R3: FAIL - diameter/clearance check failed.
R4: PASS - top surface at z=110 and no material above for x>=8.
R5: PASS - 2.535 MPa <= 20 MPa.
R6: PASS - 0.274 mm <= 2.0 mm.
R7: FAIL - 228.16 g > 90 g.

## Problems
- Mass: Current mass is 228.16 g, must be <= 90 g.
- Envelope (Y): Y range is [-25, 25], must be within [-20, 20].
- Screw Holes: Diameter/clearance requirements not met.

SIM_CODE_ISSUE: no