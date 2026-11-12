## Verdicts
R1: FAIL - The part consists of 3 separate solids.
R2: PASS - Bounding box is within limits and touches the wall.
R3: FAIL - Screw hole clearance requirements for $x \ge 10$ are not met.
R4: FAIL - Fill fraction at the shelf support ($x=140$ to $150$) is only 0.72, not solid material.
R5: PASS - Bending stress is $\approx 0.26\text{ MPa} \le 20\text{ MPa}$.
R6: PASS - Deflection is $\approx 0.009\text{ mm} \le 2.0\text{ mm}$.
R7: FAIL - Mass is $156.47\text{ g}$, exceeding the $90\text{ g}$ limit.

## Problems
- Mass: Current mass is $156.47\text{ g}$; must be $\le 90\text{ g}$.
- Geometry Integrity: Part consists of 3 solids; must be 1 single valid solid.
- Screw Access: Clearance for screwdriver at $x \ge 10$ fails R3 requirements.
- Shelf Support: Material density between $x=140$ and $150$ is $0.72$; must be a solid surface (fill fraction 1.0).

SIM_CODE_ISSUE: no