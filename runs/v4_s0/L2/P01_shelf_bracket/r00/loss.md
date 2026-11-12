R1: PASS - Found 1 solid.
R2: FAIL - Bounding box y-range is [0.0, 30.0], which exceeds the required [-20, 20].
R3: FAIL - Measured hole diameter and screwdriver clearance are 0.0.
R4: FAIL - Shelf existence at z=110 is False.
R5: UNSURE - Simulation results judged not faithful to specification.
R6: UNSURE - Simulation results judged not faithful to specification.
R7: FAIL - Mass is 119.34 g, which exceeds the limit of 90 g.

Most important problems:
- Mass: Current mass is 119.34 g; must be <= 90 g.
- Envelope (Y): Y-range is [0, 30]; must be within [-20, 20].
- Screw Holes/Access: Diameter and clearance measured as 0.0; must meet R3 dimensions.
- Shelf Support: No material found at z=110; must have horizontal surface at exactly z=110 reaching x=150.

SIM_CODE_ISSUE: yes