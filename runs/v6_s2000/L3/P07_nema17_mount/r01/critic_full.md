## Working
- R1: Simulation confirms 1 solid. PASS.
- R2: Simulation confirms face plate thickness and material around bore. PASS.
- R3: Simulation probe at (0, y, 30) shows only ~0.4mm of walled area instead of a 22.5mm diameter hole. The hole is effectively missing or incorrectly sized. FAIL.
- R4: Simulation probed the four specified coordinates for motor screw holes and found 0/4 valid holes. FAIL.
- R5: Simulation confirms zero interference with the motor clearance volume. PASS.
- R6: Simulation shows $z_{min}=0$ (correct), but probes for the two $\varnothing 5.5$ mm vertical holes at $(\pm 25, 25)$ found 0/2 holes. FAIL.
- R7: Bounding box check: $x \in [-35, 35]$ is PASS. $z_{max} = 55.24$, which exceeds the requirement of $\le 55$ mm. Mass is 55.2g (PASS). However, because $z_{max}$ fails, R7 is FAIL.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms thickness and material presence.
R3: FAIL - Bore diameter is not 22.5 mm (measured ~0.4 mm).
R4: FAIL - Zero motor screw holes found at specified coordinates.
R5: PASS - No interference with clearance volume.
R6: FAIL - Zero vertical mounting holes found at specified coordinates.
R7: FAIL - Top height is 55.24 mm, exceeding the 55 mm limit.

## Problems
- R3/R4: Motor interface - Central bore and four screw holes are missing or incorrectly sized.
- R6: Base plate - Two $\varnothing 5.5$ mm mounting holes are missing at $(\pm 25, 25)$.
- R7: Envelope - Top height is 55.24 mm; must be $\le 55$ mm.

SIM_CODE_ISSUE: no