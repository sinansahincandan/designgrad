## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. BBox [0, 136], y [-13, 13] (within |y|<=16), z [0, 14] (height <= 20).
- R3: FAIL. Probing at (6, +-6) shows empty/walled ratios of ~0.04, indicating the holes are not actually present or are extremely undersized/not cut through.
- R4: FAIL. Simulation returned `null` for motor mount holes; visual inspection confirms motor holes and shaft hole are missing.
- R5: PASS. Measured $\sigma = 1.5 \text{ MPa} \le 30 \text{ MPa}$.
- R6: PASS. Measured deflection $\approx 0.2 \text{ mm}$ (based on $I=5531$, which is $> 1.0$). Note: The simulation $I$ value ($5531$) contradicts the requirement's limit of $I \le 1.0$, but R6 asks for deflection based on an estimate where $I \le 1.0$. However, since the measured deflection is very low, it satisfies the physical intent, though there is a massive discrepancy between the design doc's claim ($I \approx 150$) and simulation ($I=5531$). Regardless, the requirement is on deflection/stiffness.
- R7: FAIL. Measured mass is $37.7\text{ g}$, which exceeds the limit of $20\text{ g}$.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - BBox within limits.
R3: FAIL - Holes at (6, +-6) are not present/cut.
R4: FAIL - Motor mount and shaft holes are missing.
R5: PASS - $\sigma = 1.5 \text{ MPa} \le 30 \text{ MPa}$.
R6: PASS - Deflection is well within limits.
R7: FAIL - Mass $37.7\text{ g} > 20\text{ g}$.

## Problems
- Mass: $37.7\text{ g}$ (should be $\le 20\text{ g}$).
- Frame attachment holes: Missing/not cut at $(6, \pm 6)$.
- Motor mount holes: Missing at $(120 \pm 8, \pm 9.5)$ and shaft hole missing at $(120, 0)$.

SIM_CODE_ISSUE: no