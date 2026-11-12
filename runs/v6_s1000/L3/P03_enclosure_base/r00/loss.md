## Verdicts
R1: PASS - Evidence R1 simulation confirms 1 solid.
R2: PASS - Evidence R2 simulation confirms floor thickness and area.
R3: PASS - Evidence R3 simulation confirms cavity is clear.
R4: PASS - Evidence R4 simulation confirms dimensions and height.
R5: FAIL - Evidence R5 simulation shows pilot holes are not empty (`hole_empty: 0.0`).
R6: PASS - Evidence R6 simulation confirms cutout presence.
R7: PASS - Evidence R7 simulation confirms mass is 66.246 g.

## Problems
- R5: Screw boss pilot holes are not open (contain material).
- R6: USB-C cutout volume in simulation (4.5 mm3) is inconsistent with a 9x3mm opening through a 2.5mm wall (should be ~67.5 mm3).

SIM_CODE_ISSUE: yes