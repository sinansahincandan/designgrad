## Verdicts
R1: PASS - Measured 1 solid.
R2: PASS - Floor thickness and coverage verified.
R3: PASS - Cavity volume is empty.
R4: PASS - Dimensions 85x55x31 match requirements.
R5: FAIL - Bosses start at z=2, but requirement R5 requires them to go from the floor (z=0).
R6: FAIL - Simulation shows empty_ratio of 0.0, meaning no cutout void was created.
R7: PASS - Mass is ~31.86g.

## Problems
- USB-C Cutout: The cutout at $x=-42.5$ has no void (empty_ratio 0.0). It must have a 9mm (Y) x 3mm (Z) opening.
- Screw Bosses: Bosses start at z=2, but must extend from the floor (z=0).

SIM_CODE_ISSUE: no