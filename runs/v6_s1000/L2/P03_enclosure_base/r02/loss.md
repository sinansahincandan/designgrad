## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor volume matches requirement.
R3: PASS - Cavity is empty.
R4: PASS - Dimensions and height are within spec.
R5: FAIL - Pilot holes are not open at the top (z=8) as they only extend from z=3.5 to z=8.
R6: FAIL - Simulation shows significant wall material remains in the cutout probe volume.
R7: PASS - Mass is 66.38 g.

## Problems
- USB-C Cutout: The R6 cutout fails to clear the wall material (simulation shows 307.5 mm³ of material remaining).
- Screw Boss Pilot Holes: The holes are not open at the top; they extend from $z=3.5$ to $z=8$, leaving the top surface solid. They must be open at $z=8$.

SIM_CODE_ISSUE: no