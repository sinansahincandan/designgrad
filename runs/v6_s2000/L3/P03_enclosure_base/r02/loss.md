## Verdicts
R1: PASS - Simulation shows 1 solid.
R2: PASS - Floor thickness verified via intersection.
R3: FAIL - Simulation detected $600.5 \text{ mm}^3$ of material in the board space.
R4: PASS - Bounding box matches dimensions and height.
R5: FAIL - Simulation reports holes are not open; render shows bosses incorrectly positioned at $z=10$.
R6: FAIL - Simulation and render show no cutout exists in the $-X$ wall.
R7: PASS - Mass is $67.1\text{ g} \le 70\text{ g}$.

## Problems
- Board Space: Material found in region $8 \le z \le 32$; should be $0 \text{ mm}^3$.
- Screw Bosses: Positioned at $z=10$ (center) instead of extending from $z=0$ to $z=8$; pilot holes are not open at the top.
- USB-C Cutout: Missing from $-X$ wall; should be a $9 \times 3\text{ mm}$ opening.

SIM_CODE_ISSUE: no