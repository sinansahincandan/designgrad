## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Floor thickness and coverage verified by intersection test.
- R3: PASS. Board cavity volume is 0, meaning no material exists in the specified region.
- R4: PASS. Dimensions (85x55) and height (31) are within spec.
- R5: FAIL. Simulation probe shows both OD and hole requirements failed at all four locations. The design document claims OD=6.0mm and a 4mm deep hole, but the measured evidence explicitly states `od_ok: false` and `hole_ok: false`.
- R6: FAIL. Simulation reports `void_vol: 0.0`, meaning no material was actually removed to create the cutout. The design document claims a subtraction occurred, but the measurement shows the volume of the void is zero.
- R7: PASS. Mass is 64.99g, which is $\le$ 70g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor thickness and coverage verified.
R3: PASS - Board cavity is empty.
R4: PASS - Dimensions are within tolerance.
R5: FAIL - Measured OD and pilot hole depth/diameter do not meet requirements.
R6: FAIL - Measured void volume is 0.0, meaning no cutout exists.
R7: PASS - Mass is 64.99g.

## Problems
- USB-C Cutout: The cutout does not exist (void volume = 0.0 mm³); it must be at least 9mm wide and 3mm high.
- Screw Bosses: Outer diameter is less than 6 mm and pilot hole depth/diameter are incorrect.

SIM_CODE_ISSUE: no