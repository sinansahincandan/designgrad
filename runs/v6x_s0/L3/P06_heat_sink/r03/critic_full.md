## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. BBox shows 40x40 mm footprint and 22 mm height, centered at origin.
- R3: PASS. Intersection volume in z=[0,3] matches the expected base volume (40x40x3 minus holes).
- R4: PASS. Measured area $A = 0.016299 \text{ m}^2$ results in $R \approx 7.22 \text{ K/W}$, which is $\le 9$.
- R5: FAIL. The simulation reports `empty_ratio: 0.0` and `clearance_vol: 0.0`, meaning the required clearance volume above the base ($z \ge 3$) does not exist or was not successfully subtracted. Furthermore, the visual review confirms that the clearance voids are offset from the mounting hole axes (at $\pm 13.49$ instead of $\pm 15$), failing both the location and the screwdriver access requirement.
- R6: PASS. Measured mass is 44.61 g, which is $\le 45$ g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - BBox shows 40x40x22 mm centered at origin.
R3: PASS - Base volume matches expected geometry for $z \in [0,3]$.
R4: PASS - Measured $R = 7.218 \text{ K/W} \le 9$.
R5: FAIL - Clearance voids are offset from hole axes and simulation shows zero clearance volume above the base.
R6: PASS - Measured mass is 44.61 g $\le 45$ g.

## Problems
- Screw clearance: The cylindrical voids are centered at approximately $(\pm 13.49, \pm 2.5)$ instead of $(\pm 15, 0)$.
- Screwdriver access: No material was successfully removed above the base ($z \ge 3$) to provide the required 3 mm radius clearance.

SIM_CODE_ISSUE: no