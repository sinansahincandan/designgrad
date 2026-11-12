## Working
- R1: PASS. Simulation confirms 1 solid in STEP file.
- R2: PASS. BBox [x:-50 to 50, y:-45 to 45, z:0 to 110] is within limits (100x100 footprint and height <= 120).
- R3: FAIL. Simulation shows 181 points of the phone volume are inside the stand mesh. The boolean subtraction failed or was insufficient.
- R4: FAIL. Design document claims brace at $a \in [70, 90]$, but specification requires $a \in [90, 110]$. Furthermore, simulation shows 0.0 volume fraction in the required region ($a \in [90, 110], b \in [-2, 0]$), and the visual reviewer confirms the brace is missing.
- R5: PASS. Simulation confirms material presence in seat and lip regions.
- R6: PASS. Combined COM $x = -25.78$ is within the footprint $x \in [-50, 50]$. The margin to the edge is $|-50 - (-25.78)| = 24.22\text{ mm}$, which is $> 5\text{ mm}$.
- R7: PASS. Mass is $\approx 45.9\text{ g}$, which is $\le 60\text{ g}$.

## Verdicts
R1: PASS - Counted 1 solid in STEP file.
R2: PASS - BBox within 100x100 footprint and height <= 120mm.
R3: FAIL - Point-in-mesh sampling found 181 points of intersection.
R4: FAIL - Simulation shows 0.0 volume in the required region $a \in [90, 110]$.
R5: PASS - Volume fraction sampling confirms seat and lip presence.
R6: PASS - Combined COM projects into footprint with $> 5\text{mm}$ margin.
R7: PASS - Mass is $\approx 45.9\text{ g} \le 60\text{ g}$.

## Problems
- R3 (Interference): The stand intersects the phone volume at 181 sampled points.
- R4 (Back support): Material is missing in the required region $a \in [90, 110], b \in [-2, 0]$.

SIM_CODE_ISSUE: no