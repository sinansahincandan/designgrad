## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. BBox shows $40 \times 40 \times 22$ mm, centered at origin.
- R3: PASS. Intersection volume in $z=[0,3]$ matches the expected base volume.
- R4: PASS. Measured $R = 7.218$ K/W is $\le 9$ K/W.
- R5: FAIL. The simulation data shows `clearance_vol: 0.0` and `empty_ratio: 0.0`, meaning the required cylindrical voids for screwdriver access (3 mm radius around the axis for $z \ge 3$) are not present or do not contain empty space. The visual review confirms the clearance voids are not continuous cylinders from $z=3$ to the top, but rather disconnected or misplaced features.
- R6: PASS. Measured mass is 44.61 g, which is $\le 45$ g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - BBox matches $40 \times 40 \times 22$ mm.
R3: PASS - Base volume at $z=[0,3]$ is correct.
R4: PASS - Measured $R = 7.218$ K/W $\le 9$ K/W.
R5: FAIL - Simulation shows zero clearance volume; visual review confirms voids are not continuous cylinders from $z=3$ to the top.
R6: PASS - Measured mass is 44.61 g $\le 45$ g.

## Problems
- R5: Screw clearance voids are not continuous cylindrical cutouts from $z=3$ to $z=22$; they appear as disconnected or misplaced features.

SIM_CODE_ISSUE: no