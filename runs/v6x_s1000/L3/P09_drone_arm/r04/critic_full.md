## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Bounding box [0, 130], y[-10, 10], z[0, 18] is within limits.
- R3: FAIL. Simulation probe shows holes at (6, +-6) are missing/diameter 0. Render confirms holes are not visible.
- R4: FAIL. Simulation probe shows motor bolt holes and shaft hole are missing. Render confirms they are missing.
- R5: FAIL. Measured stress $\sigma = 223.46$ MPa exceeds the limit of $30$ MPa. The design is too thin.
- R6: FAIL. Requirement is $I \le 1.0$. Measured $I = 47.79$. Also, deflection estimate was calculated using this incorrect $I$.
- R7: PASS. Mass $7.04$ g $\le 20$ g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Bounding box is within limits.
R3: FAIL - Probed holes at (6, +-6) are missing.
R4: FAIL - Motor bolt holes and shaft clearance hole are missing.
R5: FAIL - Measured stress 223.46 MPa > 30 MPa.
R6: FAIL - Measured I = 47.79 > 1.0.
R7: PASS - Mass 7.04 g <= 20 g.

## Problems
- Strength/Stiffness Conflict: The geometry fails both R5 and R6; the section at x=20 has $I=47.79$ (should be $\le 1.0$) and $\sigma=223.46$ MPa (should be $\le 30$ MPa).
- Motor Mount: Holes at $(120 \pm 8, \pm 9.5)$ and shaft hole at $(120, 0)$ are missing.
- Frame Attachment: Vertical holes at $(6, \pm 6)$ are missing.
- Geometry Discrepancy: The motor mount (x=110 to 130) is not a widened flange as described in the design document.

SIM_CODE_ISSUE: no