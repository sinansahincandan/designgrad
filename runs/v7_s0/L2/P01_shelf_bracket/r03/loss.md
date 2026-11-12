## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Simulation shows holes/clearance are not present or valid.
R4: FAIL - Fill fraction at $x \in [140, 150], z \approx 110$ is only 0.5, not solid.
R5: PASS - Stress 0.55 MPa $\le$ 20 MPa.
R6: PASS - Deflection 0.02 mm $\le$ 2.0 mm.
R7: PASS - Mass 75.3 g $\le$ 90 g.

## Problems
- R4: Shelf support thickness/solidity at $x \in [140, 150]$ is 50% (fill fraction 0.5); must be 100% solid material below $z=110$.
- R3: Screw holes and screwdriver access are missing or incorrectly implemented according to simulation results.

SIM_CODE_ISSUE: no