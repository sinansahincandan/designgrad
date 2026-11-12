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