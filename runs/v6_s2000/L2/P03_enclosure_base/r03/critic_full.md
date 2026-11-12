## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Floor thickness is verified as at least 2mm (z=0 to z=8).
- R3: FAIL. The simulation shows an intersection volume of ~0.0096 in the void region, meaning material exists where it should be free. Specifically, the design document states bosses extend from $z=8$ to $z=14$, which directly violates the requirement that the region $8 \le z \le 32$ must be "completely free of material".
- R4: PASS. Dimensions are 85x55 and top is at $z=32$.
- R5: FAIL. The simulation probe at $(\pm 35, \pm 20)$ failed on all counts (OD, hole presence/location, wall thickness). The design document states bosses extend from $z=8$ up to $z=14$, but the requirement R5 specifies they must extend "from the floor up to z = 8". By extending into the board space ($z>8$), they violate R3 and fail the probe check for being at the correct Z-range.
- R6: PASS. Cutout is present and sized correctly.
- R7: PASS. Mass is 67.53g, which is $\le$ 70g.

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