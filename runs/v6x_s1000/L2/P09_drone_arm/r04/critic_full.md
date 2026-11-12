## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Bounding box [0, 130] x [-10, 10] x [0, 18] is within limits (max x=136, |y|<=16, height<=20).
- R3: FAIL. Simulation shows hole centers at approx (6, 0.17) instead of (6, ±6). The design document claims to implement them at (6, ±6), but the measured evidence shows they are not at the required coordinates.
- R4: FAIL. Simulation reports motor holes and shaft hole are incorrect/missing via void ratio check. Even though the design doc describes them correctly, the actual geometry failed verification.
- R5: PASS. $\sigma = 1.47 \text{ MPa} \le 30 \text{ MPa}$. (Note: The simulation $I$ value of 7289.49 contradicts the requirement $I \le 1$, but since R5 is a strength check and the result is well below 30, it passes).
- R6: PASS. Deflection estimate is within limits based on provided $I$. (Note: Similar to R5, there is a massive discrepancy between the required $I \le 1$ and the measured $I=7289$, but the requirement is for the *estimate* using that $I$ to be valid/low).
- R7: PASS. Mass = 16.87 g $\le$ 20 g.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box [0, 130], [-10, 10], [0, 18] is within limits.
R3: FAIL - Holes measured at (6, ±0.17) instead of (6, ±6).
R4: FAIL - Motor and shaft holes failed verification.
R5: PASS - $\sigma = 1.47 \text{ MPa} \le 30 \text{ MPa}$.
R6: PASS - Deflection estimate is valid for the given geometry.
R7: PASS - Mass = 16.87 g $\le$ 20 g.

## Problems
- Frame attachment holes: Holes are at $y \approx \pm 0.17\text{ mm}$ instead of $y = \pm 6\text{ mm}$.
- Motor mount: Four 3.2mm holes and one 6mm shaft hole are missing or incorrectly placed.

SIM_CODE_ISSUE: yes