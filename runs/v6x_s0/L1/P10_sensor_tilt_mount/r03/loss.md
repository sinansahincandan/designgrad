## Verdicts
R1: UNSURE - No valid code was produced to verify geometry.
R2: PASS - Matches specification.
R3: PASS - Area $1050 \ge 900$.
R4: PASS - Height $42.5$ is in $[35, 50]$.
R5: PASS - Matches specification.
R6: FAIL - Sensor CoM $y = 27.99$ mm exceeds the stability limit of $15$ mm (base edge $20$ mm minus $5$ mm margin).
R7: PASS - Mass $\approx 2.85\text{ g} \le 35\text{ g}$.

## Problems
- Stability (R6): The base footprint $y$-range is $[-20, 20]$. With the required $5$ mm margin, the CoM must be $\le 15$. The sensor CoM is at $y = 27.99$. The base must extend to at least $y = 32.99$ or the face center $y$ must be moved back.
- Code Execution: The `rotate` method call in the CadQuery script is missing the angle argument, preventing design verification.