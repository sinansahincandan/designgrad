## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Bounding box [0, 160] x [0, 20] x [0, 110] fits within limits. Note: $y$ range is $[0, 20]$, which satisfies the envelope $-20 \le y \le 20$.
- R3: FAIL. Simulation reports holes do not exist (existence ratio < 0.05). The design document claims to subtract cylindrical voids and rectangular prisms, but the simulation shows no hole geometry at the specified coordinates.
- R4: FAIL. Requirement specifies a horizontal top surface at *exactly* $z=110$ with solid material directly below it between $x=140$ and $x=150$. Simulation shows a fill fraction of only 0.50 in that region, meaning the shelf support is not fully solid as required.
- R5: PASS. Measured stress $\sigma = 0.55 \text{ MPa}$ is well below $20 \text{ MPa}$.
- R6: PASS. Measured deflection $\delta = 0.02 \text{ mm}$ is well below $2.0 \text{ mm}$.
- R7: PASS. Measured mass $76.09\text{g}$ is below $90\text{g}$.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Holes at (y=0, z=20) and (y=0, z=60) are not detected in the geometry.
R4: FAIL - Fill fraction at x[140,150], y[-1,1], z[108,110] is 0.50; must be 1.0 for solid support.
R5: PASS - Stress 0.55 MPa <= 20 MPa.
R6: PASS - Deflection 0.02 mm <= 2.0 mm.
R7: PASS - Mass 76.09 g <= 90 g.

## Problems
1. Screw Holes: The cylindrical voids at (y=0, z=20) and (y=0, z=60) are missing from the geometry.
2. Shelf Support: The material between $x=140$ and $x=150$ below $z=110$ is only 50% solid; it must be a continuous solid to support the shelf.

SIM_CODE_ISSUE: no