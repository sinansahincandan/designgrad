## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor thickness (8mm) exceeds 2mm minimum.
R3: FAIL - Simulation indicates the board space is not empty.
R4: PASS - Measured dimensions 86 x 56 mm are within the $85 \pm 1.5$ mm tolerance.
R5: FAIL - Simulation reports holes are not open at the top; visual evidence shows incorrect Y-position.
R6: FAIL - Simulation and visual evidence confirm the USB-C cutout is missing.
R7: PASS - Measured mass 66.45 g is $\le$ 70 g.

## Problems
- USB-C Cutout: Missing from -X wall; should be a $9 \times 3$ mm aperture at $y=0, z=14$.
- Screw Bosses: Holes are not open at the top (z=8); pilot holes must be open to the top.
- Screw Bosses: Y-position is $\pm 27.83$; should be $\pm 20$.
- Board Space: Region $-40 \le x \le 40, -25 \le y \le 25, 8 \le z \le 32$ contains material; must be completely free.

SIM_CODE_ISSUE: no