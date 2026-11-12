## Verdicts
R1: PASS - Simulation confirms one solid.
R2: PASS - Bounding box is within specified limits.
R3: FAIL - Simulation shows screw holes do not exist and screwdriver access is insufficient.
R4: FAIL - Fill fraction at $x \in [140, 150], z \in [100, 110]$ is 0.8 instead of 1.0.
R5: PASS - Measured stress 0.56 MPa $\le$ 20 MPa.
R6: PASS - Measured deflection 0.02 mm $\le$ 2.0 mm.
R7: PASS - Measured mass 59.22 g $\le$ 90 g.

## Problems
- Screw Holes (R3): The holes at $(y=0, z=20)$ and $(y=0, z=60)$ are not present in the geometry, and screwdriver access channels do not provide clearance from the front.
- Shelf Support (R4): Material density between $x=140$ to $150$ at $z \in [100, 110]$ is 0.8; it must be 1.0 (solid).

SIM_CODE_ISSUE: no