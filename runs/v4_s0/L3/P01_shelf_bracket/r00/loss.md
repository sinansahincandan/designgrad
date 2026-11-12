R1: PASS - Found 1 solid.
R2: FAIL - Bounding box y-range is [0.0, 30.0], which violates the required range [-20, 20].
R3: FAIL - Screw hole axes are along Y instead of X; holes are centered at y=1.75 instead of y=0.
R4: FAIL - Shelf existence at z=110 is False (no material found at that height).
R5: UNSURE - Simulation results for stress are judged not faithful to the specification.
R6: UNSURE - Simulation results for deflection are judged not faithful to the specification.
R7: FAIL - Mass is 119.34g, which exceeds the limit of 90g.

Most important problems to fix:
- Screw holes: Axis must be along X and centered at y=0 (currently Y axis and y=1.75).
- Envelope: Y-range must be [-20, 20] (currently [0, 30]).
- Shelf support: Material must exist at z=110 reaching x=150 (currently no material at z=110).
- Mass: Must be <= 90g (currently 119.34g).

SIM_CODE_ISSUE: yes