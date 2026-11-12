## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Floor thickness is 8mm.
R3: FAIL - Material detected in the void region (intersection volume > 0).
R4: PASS - Dimensions are 85x55x32.
R5: FAIL - Bosses extend into the board space ($z=8$ to $14$) instead of being contained within the floor ($z \le 8$).
R6: PASS - Cutout is present and correctly sized.
R7: PASS - Mass is 67.53g.

## Problems
- Boss placement/height: Bosses extend from $z=8$ to $z=14$; they must be contained within the floor ($z \le 8$) to satisfy R3 and R5.
- Board space violation: Material exists in the region $8 \le z \le 32$ due to the protruding bosses.

SIM_CODE_ISSUE: no