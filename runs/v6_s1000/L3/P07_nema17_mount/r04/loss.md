## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Simulation shows insufficient material around the central bore.
R3: FAIL - Simulation shows the central bore is not a valid void.
R4: FAIL - Simulation shows motor screw holes are not valid voids.
R5: PASS - Simulation confirms no intersection with clearance volume.
R6: FAIL - Simulation shows base does not sit at $z=0$ and holes are malformed.
R7: PASS - Envelope and mass are within limits.

## Problems
- Face Plate Integrity (R2): Material is missing around the central bore; must have solid material in the ring surrounding the bore.
- Central Bore (R3): The $\varnothing 22.5$ mm hole is not a valid void through the face plate.
- Motor Screw Holes (R4): The four $\varnothing 3.4$ mm holes are not valid voids through the face plate.
- Base Placement (R6): The base does not sit on the table; $z_{min}$ is $0.042$ instead of $0$.

SIM_CODE_ISSUE: no