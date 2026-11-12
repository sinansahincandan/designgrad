## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. BBox $x \approx 98.8$, $y=90$, $z_{max}=100$, $z_{min}=0$. All within limits ($100, 100, 120$).
- R3: FAIL. Point-in-mesh sampling shows intersection (value 210.0). The design claims to use a $-0.5\text{mm}$ offset, but the simulation proves it fails to prevent intersection with the phone volume.
- R4: FAIL. Sampling in the required region ($a \in [90, 110]$) returned $0.0$ volume fraction. The design placed the brace at $a \in [75, 95]$, which only partially covers the required range and fails to provide material in the critical $[95, 110]$ segment.
- R5: PASS. Volume sampling confirms presence of seat and lip in specified regions.
- R6: PASS. Combined COM is at $x \approx -20$. Footprint $x$ is $[-48.8, 50]$. Margin to edge is $|-48.8 - (-20)| = 28.8\text{mm}$ and $|50 - (-20)| = 70\text{mm}$. Both $> 5\text{mm}$.
- R7: FAIL. Measured mass is $88.1\text{g}$, which exceeds the $60\text{g}$ limit. The design's estimate of $43.4\text{g}$ was incorrect; actual volume is $71,052.97 \text{ mm}^3$.

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