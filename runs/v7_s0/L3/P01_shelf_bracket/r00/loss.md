## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Y-envelope [0, 30] exceeds required [-20, 20].
R3: FAIL - Screw axes are along Y instead of X; holes are offset from y=0.
R4: FAIL - Material density at $x \in [140, 150]$ is only 0.5, not solid.
R5: PASS - Measured stress 0.38 MPa $\le$ 20 MPa.
R6: PASS - Measured deflection 0.01 mm $\le$ 2.0 mm.
R7: FAIL - Measured mass 119.34g exceeds 90g limit.

## Problems
- Mass: Current 119.34g, should be $\le$ 90g.
- Screw Holes: Axis is along Y, should be along X; center $y=1.75$, should be $y=0$.
- Shelf Support: Fill fraction at $x \in [140, 150]$ is 0.5, should be 1.0 (solid).
- Envelope: Y-range is $[0, 30]$, should be within $[-20, 20]$.

SIM_CODE_ISSUE: no