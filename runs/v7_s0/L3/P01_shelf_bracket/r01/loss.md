## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: PASS - Bounding box is within specified limits.
R3: FAIL - Simulation confirms screw holes do not exist.
R4: FAIL - Simulation shows fill fraction of 0.8 in the required support volume, indicating a void.
R5: PASS - Measured stress 0.54 MPa $\le$ 20 MPa.
R6: PASS - Measured deflection 0.02 mm $\le$ 2.0 mm.
R7: PASS - Measured mass 60.6 g $\le$ 90 g.

## Problems
- Screw Holes: R3 holes at (y=0, z=20) and (y=0, z=60) are missing from the geometry.
- Shelf Support: Material is missing in the volume $x \in [140, 150], y \in [-1, 1], z \in [100, 110]$ (fill fraction 0.8 instead of 1.0).

SIM_CODE_ISSUE: no