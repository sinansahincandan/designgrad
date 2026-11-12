## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Bounding box [0, 160] x [0, 20] x [0, 110] is within limits and touches $x=0$. Note: the design says centered on $y=0$ ($-10$ to $10$), but simulation shows $y \in [0, 20]$. This still fits $-20 \le y \le 20$.
- R3: FAIL. Simulation reports holes do not exist or clearance is not met (`exists: false`). The design claims cutouts from $x=10$ to $x=15$, but the simulation indicates a failure in hole existence/access.
- R4: FAIL. Requirement requires solid material directly below $z=110$ between $x=140$ and $150$. Simulation shows a fill fraction of only 0.5 (50%) at that location, meaning it is not "solid" as required.
- R5: PASS. Measured stress $\approx 0.55 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. Measured deflection $\approx 0.02 \text{ mm} \le 2.0 \text{ mm}$.
- R7: PASS. Measured mass $\approx 75.3\text{g} \le 90\text{g}$.

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