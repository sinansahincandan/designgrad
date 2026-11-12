## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box $y$ range is $[-10, 40]$. Requirement is $[-20, 20]$. The part is offset and exceeds the width limit.
- R3: FAIL. Simulation shows `empty_ratio` of 0.0 for holes/clearance (implying no material was removed or clearance was not provided correctly) and only one cylindrical face found at $z=60$. Requirement needs two holes and specific screwdriver clearance for $x \ge 10$.
- R4: PASS. Top surface is at $z=110$ and nothing is above it for $x \ge 8$.
- R5: PASS. $\sigma = 0.26\text{ MPa} \le 20\text{ MPa}$.
- R6: PASS. $\delta = 0.0089\text{ mm} \le 2.0\text{ mm}$.
- R7: FAIL. Mass is $444.84\text{ g}$, which is much greater than the limit of $90\text{ g}$.

## Verdicts
R1: PASS - Simulation confirms one solid.
R2: FAIL - Bounding box y-range is [-10, 40], must be within [-20, 20].
R3: FAIL - Simulation indicates screw hole/clearance requirements not met.
R4: PASS - Top surface at z=110 and no material above for x>=8.
R5: PASS - Bending stress 0.26 MPa <= 20 MPa.
R6: PASS - Deflection 0.009 mm <= 2.0 mm.
R7: FAIL - Mass is 444.84 g, must be <= 90 g.

## Problems
- Mass: Current mass 444.84 g, should be <= 90 g.
- Envelope (Y): Y-range [-10, 40], should be within [-20, 20].
- Screw Access: Missing required screw holes and screwdriver clearance for x >= 10.

SIM_CODE_ISSUE: no