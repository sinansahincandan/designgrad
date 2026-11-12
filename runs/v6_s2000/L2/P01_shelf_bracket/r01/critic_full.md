## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Bounding box [0, 150] x [-20, 20] x [0, 110] fits within the required envelope and touches $x=0$.
- R3: FAIL. The simulation reports `clearance_vol = 0` for the screw holes at $x \ge 10$, meaning no screwdriver clearance was successfully modeled/subtracted as required.
- R4: FAIL. While the volume above $z=110$ is correct (0.0), the fill fraction in the required support zone ($x \in [140, 150]$, $y \in [-5, 5]$, $z \in [105, 110]$) is only 0.8. The requirement requires "solid material directly below $z=110$ between $x=140$ and $150$ around $y=0$". A fill fraction of 0.8 implies the surface is not a continuous solid slab in that region.
- R5: PASS. $\sigma = 1.37 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. $\delta = 0.0377 \text{ mm} \le 2.0 \text{ mm}$.
- R7: PASS. Mass $42.85 \text{ g} \le 90 \text{ g}$.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - clearance_vol is 0 for x >= 10.
R4: FAIL - fill fraction in support zone is 0.8, not 1.0.
R5: PASS - sigma = 1.37 MPa <= 20 MPa.
R6: PASS - delta = 0.0377 mm <= 2.0 mm.
R7: PASS - mass = 42.85 g <= 90 g.

## Problems
- Screw Clearance (R3): The clearance volume for $x \ge 10$ is 0; it must be non-zero to allow screwdriver access.
- Shelf Support (R4): Fill fraction in the support zone ($x=140\text{--}150, y \approx 0, z \approx 110$) is 0.8; it must be 1.0 for a continuous solid surface.

SIM_CODE_ISSUE: no