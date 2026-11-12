## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Y extent is 42.5 mm (req: 18-22) and Zmin is -15.5 (req: z=0).
R3: FAIL - Intersection volume ratio is 0.035, meaning pipe volume is not free of material.
R4: FAIL - Point sampling shows 0.0 material in the required band.
R5: FAIL - Simulation indicates holes are not correctly placed/subtracted at $(\pm27, 0)$.
R6: FAIL - Sampling shows only 45% coverage in the flange region.
R7: PASS - Mass is 11.387 g (req: $\le 25$ g).

## Problems
- Clamp Width: Y extent is 42.5 mm; should be between 18 and 22 mm.
- Mounting Surface: Zmin is -15.5 mm; must sit on z = 0.
- Pipe Clearance: Material exists in the pipe volume (intersection ratio 0.035); must be free of material.
- Upper Band: No material found in the band $|x| \le 7$ at radius $12.7\text{--}15.5$ mm.
- Flanges: Only 45% solid coverage in specified region; must be fully solid from z=0 to 3.
- Screw Holes: Holes are not correctly subtracted at $(\pm27, 0)$.

SIM_CODE_ISSUE: no