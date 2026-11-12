## Working
- R1: PASS. Evidence shows 1 solid.
- R2: FAIL. The BBox x-max is 150, but the requirement says it must reach at least $x=150$ (implied by R4/R5) and the design concept claims extension to $x=160$. However, the measured BBox shows $x \in [0, 150]$. More critically, the Y-range is $[0, 30]$, which violates the requirement $-20 \le y \le 20$ (width must be centered or within that range; here it is entirely positive).
- R3: UNSURE. The simulation for this was judged not faithful and cannot be relied upon.
- R4: FAIL. Shelf presence check returned False. The requirement requires solid material directly below $z=110$ between $x=140$ and $150$.
- R5: UNSURE. Simulation is judged not faithful due to impossible Moment of Inertia values.
- R6: UNSURE. Simulation is judged not faithful due to impossible Moment of Inertia values.
- R7: FAIL. Measured mass is 119.34 g, which exceeds the limit of 90 g.

## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: FAIL - Y-dimension [0, 30] exceeds range [-20, 20].
R3: UNSURE - Simulation not faithful.
R4: FAIL - No material found at the required shelf support location.
R5: UNSURE - Simulation not faithful.
R6: UNSURE - Simulation not faithful.
R7: FAIL - Mass is 119.34 g, exceeding 90 g limit.

## Problems
- Mass: Current mass is 119.34 g; must be $\le$ 90 g.
- Shelf Support: No material found at $z=110$ between $x=140$ and $150$.
- Envelope (Y): Y-range is [0, 30]; must be within [-20, 20].

SIM_CODE_ISSUE: yes