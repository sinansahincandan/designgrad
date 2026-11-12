R1: PASS - Found 1 solid.
R2: FAIL - Bounding box y-range is [-10, 20], which violates the requirement of -20 <= y <= 20 (the part does not span/reach the required width or is offset).
R3: PASS - Hole diameter 5.5 mm and clearance for x >= 10 verified.
R4: PASS - Shelf exists at z=110 and no material is above z=110 for x >= 8.
R5: UNSURE - Simulation check was judged not faithful; calculation provided in design doc is suspect.
R6: UNSURE - Simulation check was judged not faithful; relies on implausible moment of inertia.
R7: PASS - Mass is 82.0 g, which is <= 90 g.

Most important problems to fix:
- Envelope (R2): The y-dimension range is [-10, 20], failing to meet the required width/positioning of -20 <= y <= 20.
- Strength/Stiffness (R5/R6): Verification failed due to unreliable simulation data; geometry must be re-validated for stress and deflection at x=10.

SIM_CODE_ISSUE: yes