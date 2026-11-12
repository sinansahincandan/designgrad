## Working
- R1: PASS. Simulation confirms 1 solid in STEP file.
- R2: FAIL. Measured x_ext = 116.38 mm (> 100 mm), z_ext = 180.64 mm (> 120 mm), and z_min = -22.43 mm (must be $\ge$ 0).
- R3: FAIL. Point-in-mesh sampling shows intersection volume of 1942.0 units.
- R4: PASS. Presence check in the specified region $a \in [90, 110]$ is successful.
- R5: PASS. Presence check for seat and lip regions is successful.
- R6: PASS. Combined COM projection falls within footprint with $>5$ mm margin.
- R7: FAIL. Measured mass is 793.43 g (calculated from volume $639859 \text{ mm}^3$), which exceeds the limit of 60 g.

## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: FAIL - x_ext=116.38mm (>100), z_ext=180.64mm (>120), and z_min=-22.43mm (<0).
R3: FAIL - Intersection volume of 1942.0 detected.
R4: PASS - Material present in specified region.
R5: PASS - Material present in seat and lip regions.
R6: PASS - COM projects within footprint with >5mm margin.
R7: FAIL - Mass is 793.43g (>60g).

## Problems
- Mass (R7): Current mass 793.43 g, should be $\le$ 60 g.
- Dimensions (R2): Height 180.64 mm, should be $\le$ 120 mm; x_ext 116.38 mm, should be $\le$ 100 mm.
- Floor Penetration (R2): z_min -22.43 mm, should be $\ge$ 0.
- Interference (R3): Intersection volume 1942.0, should be 0.

SIM_CODE_ISSUE: no