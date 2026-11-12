## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - BBox shows 40x40 footprint and 23mm height.
R3: FAIL - Probe check failed; mounting voids remove material from the base area.
R4: PASS - Measured $R = 8.89$ K/W $\le 9$.
R5: FAIL - Simulation shows one hole fails verification.
R6: PASS - Measured mass 30.37g $\le 45$g.

## Problems
- R3: Base thickness; material is removed from the base (z=0 to 3) by the mounting voids. The base must be solid over the whole footprint.
- R5: Mounting holes; one of the two holes failed verification.

SIM_CODE_ISSUE: no