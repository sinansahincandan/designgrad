## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. BBox shows 40x40 footprint and 23mm height.
- R3: FAIL. The grid-based probe check failed for the base thickness (z=0 to 3). This implies the mounting voids (which extend from z=0) have removed material from the base, violating the requirement that the base must be at least 3mm thick over the *whole* footprint.
- R4: PASS. Measured $R \approx 8.89$ K/W, which is $\le 9$.
- R5: FAIL. The simulation reports `[false, true]`. This indicates that while one hole meets requirements, the other does not. Specifically, the requirement for a 3.2mm diameter vertical through-hole was likely missed or incorrectly sized in one location, even though the $\varnothing$8mm clearance is present.
- R6: PASS. Measured mass is ~30.37g, which is $\le 45$g.

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