## Working
- R1: Simulation confirms 1 solid. PASS.
- R2: Simulation confirms volume exists in the $y \in [0,4]$ slab and design doc states thickness is 4mm. PASS.
- R3: Simulation probe at $(0, y, 30)$ with diameter 22.5 mm returns 0.0 for both empty and walled space. This means the bore does not exist where specified. FAIL.
- R4: Simulation probe for four $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$ found 0/4 valid holes. The motor screw holes are missing. FAIL.
- R5: Simulation shows 0.0 interference volume with the specified clearance box. PASS.
- R6: Simulation confirms $z_{min}=0$, but probing for two $\varnothing 5.5$ mm holes at $(\pm 25, 25)$ found 0 holes. The table mounting holes are missing. FAIL.
- R7: Bounding box is within $[-35, 35]$ and $z \le 55$. Mass is calculated as 49.9g (below 60g limit). PASS.

## Verdicts
R1: PASS - 1 solid found via simulation.
R2: PASS - Face plate thickness and material presence confirmed by simulation.
R3: FAIL - Bore diameter 22.5 mm not detected at $(0, y, 30)$ via simulation.
R4: FAIL - Zero motor screw holes detected via simulation at $(\pm 15.5, 30 \pm 15.5)$.
R5: PASS - Zero interference volume with clearance box confirmed by simulation.
R6: FAIL - Two $\varnothing 5.5$ mm mounting holes not detected via simulation at $(\pm 25, 25)$.
R7: PASS - Envelope and mass (49.9g) within limits confirmed by simulation.

## Problems
- Central bore: Diameter is 0 mm, should be 22.5 mm.
- Motor screw holes: 0/4 holes found, should be 4 holes of diameter 3.4 mm at $(\pm 15.5, 30 \pm 15.5)$.
- Base mounting holes: 0/2 holes found, should be 2 holes of diameter 5.5 mm at $(\pm 25, 25)$.

SIM_CODE_ISSUE: no