## Working
- R1: PASS. Evidence shows 1 solid.
- R2: FAIL. Bounding box Y range is [-30, 30], which exceeds the requirement of [-20, 20].
- R3: FAIL. Simulation evidence indicates failure for clearance/hole requirements (though specific details are truncated in the note, it is marked FAIL).
- R4: FAIL. Forbidden volume detected ($1358.4 \text{ mm}^3$) for $x \ge 8$ and $z > 110$. This means part of the bracket is too high.
- R5: PASS. $\sigma = 0.31 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. $\delta = 0.0095 \text{ mm} \le 2.0 \text{ mm}$.
- R7: FAIL. Mass is $350.98 \text{ g}$, which exceeds the limit of $90 \text{ g}$.

## Verdicts
R1: PASS - Found 1 solid.
R2: FAIL - Y dimension is [-30, 30], exceeding limits [-20, 20].
R3: FAIL - Simulation indicates failure for hole/clearance requirements.
R4: FAIL - Forbidden volume detected above $z=110$ for $x \ge 8$.
R5: PASS - Stress is 0.31 MPa $\le$ 20 MPa.
R6: PASS - Deflection is 0.0095 mm $\le$ 2.0 mm.
R7: FAIL - Mass is 350.98 g, exceeding limit of 90 g.

## Problems
- Mass: Current mass is 350.98 g; must be $\le$ 90 g.
- Envelope (Y): Y range is [-30, 30]; must be within [-20, 20].
- Height Constraint: Forbidden volume detected above $z=110$ for $x \ge 8$.
- Screw Hole Clearance: Failed R3 clearance/access requirements.

SIM_CODE_ISSUE: no