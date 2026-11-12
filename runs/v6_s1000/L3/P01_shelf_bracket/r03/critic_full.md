## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Bounding box [0, 150] x [-20, 20] x [0, 110] is within limits.
- R3: FAIL. Simulation reports failure for hole/clearance check at (y=0, z=20) and (y=0, z=60). The design claims to subtract a radius of 4mm, but the measurement indicates the requirement was not met.
- R4: FAIL. Simulation reports a fill ratio of ~0.047 in the region $x \in [140, 150], y \in [-2, 2], z \in [0, 110]$. This implies there is insufficient solid material directly below $z=110$ to satisfy "solid material directly below $z=110$ between $x=140$ and $150$ around $y=0$".
- R5: PASS. Measured stress $\sigma \approx 0.27$ MPa is $\le 20$ MPa.
- R6: PASS. Measured deflection $\delta \approx 0.009$ mm is $\le 2.0$ mm.
- R7: FAIL. Measured mass is 209.13 g, which exceeds the limit of 90 g. The design document's claim of 68.2 g is contradicted by the simulation measurement.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Screw hole/clearance requirements not met per simulation.
R4: FAIL - Insufficient material below z=110 in the x=[140,150] range.
R5: PASS - Stress 0.27 MPa <= 20 MPa.
R6: PASS - Deflection 0.009 mm <= 2.0 mm.
R7: FAIL - Mass 209.13 g > 90 g.

## Problems
- Mass: Current mass is 209.13 g; must be <= 90 g.
- Shelf Support: Material density at x=[140,150], y=0, below z=110 is insufficient to meet R4.
- Screw Holes: Clearance/geometry for holes at (y=0, z=20) and (y=0, z=60) failed inspection.

SIM_CODE_ISSUE: no