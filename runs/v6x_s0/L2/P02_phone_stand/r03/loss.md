## Verdicts
R1: PASS - 1 solid found.
R2: PASS - BBox within limits.
R3: FAIL - Intersection detected with phone volume.
R4: FAIL - No material in required region $a \in [90, 110]$.
R5: PASS - Seat and lip volumes present.
R6: PASS - COM projection is well within footprint margin.
R7: FAIL - Mass is 88.1g, exceeding 60g limit.

## Problems
- R7: Total mass is 88.1g; must be $\le 60\text{g}$.
- R3: Phone intersection detected; stand geometry overlaps phone volume.
- R4: Rear brace location $a \in [75, 95]$ fails to cover the required range of $a \in [90, 110]$.

SIM_CODE_ISSUE: no