## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box $x \in [0, 150]$, $y \in [0, 30]$, $z \in [0, 110]$. The requirement allows up to $x=170$ and $y \in [-20, 20]$. However, the $y$-range is $[0, 30]$, which exceeds the limit of $y_{max}=20$.
- R3: FAIL. Render evidence shows screw hole axes are along the Y axis (perpendicular to wall), whereas R3 requires axes along X (through the part). Also, holes are offset at $y=1.75$ instead of $y=0$. Simulation failed to find the holes.
- R4: FAIL. Simulation shows fill fraction at $x \in [140, 150]$ is only 0.5 (half-filled), but requirement requires solid material directly below $z=110$ in that range.
- R5: PASS. Measured stress $\sigma = 0.38 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. Measured deflection $\delta = 0.01 \text{ mm} \le 2.0 \text{ mm}$.
- R7: FAIL. Measured mass is $119.34\text{g}$, which exceeds the limit of $90\text{g}$.

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