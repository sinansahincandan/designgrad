## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Bounding box [0, 150.1] x [-20, 20] x [0, 127.5] is within limits [0, 170] x [-20, 20] x [0, 130].
- R3: FAIL. Simulation reports `clear_vol: 0.0` and failed screwdriver clearance check for the specified holes.
- R4: FAIL. Measured volume above $z=110$ for $x \ge 8$ is $54744.4\text{ mm}^3$. The design document claims height is capped at 110, but evidence shows it reaches $z=127.5$.
- R5: PASS. $\sigma = 0.326\text{ MPa} \le 20\text{ MPa}$.
- R6: PASS. $\delta = 0.01\text{ mm} \le 2.0\text{ mm}$.
- R7: FAIL. Measured mass is $169.77\text{ g}$, which exceeds the limit of $90\text{ g}$.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Screwdriver clearance/volume check failed.
R4: FAIL - Volume above $z=110$ for $x \ge 8$ is $54744.4\text{ mm}^3$.
R5: PASS - Stress is $0.326\text{ MPa}$.
R6: PASS - Deflection is $0.01\text{ mm}$.
R7: FAIL - Mass is $169.77\text{ g}$, limit is $90\text{ g}$.

## Problems
- Mass: Current mass is $169.77\text{ g}$, must be $\le 90\text{ g}$.
- Geometry Height: Part extends to $z=127.5$, must not exceed $z=110$ for $x \ge 8$.
- Screwdriver Access: Clearance volume around hole axes is insufficient/missing.

SIM_CODE_ISSUE: no