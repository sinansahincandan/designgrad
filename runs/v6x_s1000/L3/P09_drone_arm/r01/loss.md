## Verdicts
R1: FAIL - Found 3 solids instead of one single solid.
R2: FAIL - Minimum x is -2.5; must be $\ge 0$.
R3: FAIL - Holes are misplaced (centered around $y=5$ instead of $\pm 6$).
R4: FAIL - Motor mount holes are at $x=132$ instead of $x=120$.
R5: FAIL - Bending stress is 107.14 MPa; must be $\le 30$ MPa.
R6: FAIL - Moment of inertia $I$ is 21.28 mm$^4$; must be $\le 1.0$ mm$^4$.
R7: PASS - Mass is 13.19 g.

## Problems
- R6/R5 (Stiffness/Strength): Section at x=20 has $I = 21.28 \text{ mm}^4$; must be $\le 1.0 \text{ mm}^4$. This causes stress to exceed 30 MPa.
- R1: Part consists of 3 solids; must be one single solid.
- R2: Minimum x is -2.5; must be $\ge 0$.
- R4: Motor mount holes are at $x=132$; must be at $x=120 \pm 8$.
- R3: Frame attachment holes are centered near $y=5$; must be at $y = \pm 6$.

SIM_CODE_ISSUE: no