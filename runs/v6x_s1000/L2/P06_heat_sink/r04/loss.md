## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - BBox shows 40x40 footprint and 23mm height.
R3: FAIL - Grid-based probe indicates the base is not at least 3mm thick over the whole footprint (voids penetrate the base).
R4: PASS - Measured $R = 8.89$ K/W $\le 9$ K/W.
R5: FAIL - Simulation reports failure for hole existence/verification.
R6: PASS - Measured mass 30.37 g $\le$ 45 g.

## Problems
- Base Thickness: The access voids penetrate the base from $z=0$, violating the requirement for a solid base of at least 3mm thickness over the whole footprint (R3).
- Mounting Holes: The design uses $\varnothing$8 mm voids instead of the specified $\varnothing$3.2 mm holes, and simulation indicates a failure in hole verification (R5).

SIM_CODE_ISSUE: no