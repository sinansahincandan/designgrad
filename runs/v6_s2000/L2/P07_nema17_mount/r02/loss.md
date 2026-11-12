## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Evidence shows $y_{max}=50$ instead of the required thickness up to $y=4$.
R3: FAIL - Probe at $(0, y, 30)$ indicates the central bore is not present as a void.
R4: FAIL - Simulation found 0 out of 4 motor screw holes.
R5: PASS - Interference volume with clearance box is 0.0.
R6: FAIL - $z_{min}$ is $-27.5$ instead of $\ge 0$, and no screw holes were detected.
R7: PASS - Envelope and mass are within specification.

## Problems
- Base Position: $z_{min}$ is $-27.5$ mm; should be $\ge 0$.
- Face Plate Thickness/Position: $y_{max}$ is $50$ mm; should be $4$ mm.
- Motor Screw Holes: 0 holes found at $(\pm 15.5, 30 \pm 15.5)$; 4 holes of $\varnothing 3.4$ mm required.
- Central Bore: Bore not detected at $(0, y, 30)$; $\varnothing 22.5$ mm void required.
- Base Screw Holes: 0 holes found at $(\pm 25, 25)$; 2 holes of $\varnothing 5.5$ mm required.

SIM_CODE_ISSUE: no