## Working
- R1: PASS. Simulation confirms 1 solid in STEP file.
- R2: FAIL. Measured x_ext = 153.46 mm (> 100 mm limit), z_ext = 239.87 mm (> 120 mm limit), and z_min = -39.87 mm (< 0 mm requirement).
- R3: FAIL. Point-in-mesh sampling shows 1186 points of intersection between the stand and phone volume.
- R4: PASS. Volume fraction sampling confirms material presence in the specified region.
- R5: PASS. Volume fraction sampling confirms seat and lip are present in specified regions.
- R6: PASS. Combined COM projects within the footprint with the required margin.
- R7: FAIL. Measured mass is 663.77 g, which significantly exceeds the 60 g limit (measured volume was ~535,295 mm³).

## Verdicts
R1: PASS - Counted 1 solid in STEP file.
R2: FAIL - x_ext=153.46mm (>100), z_ext=239.87mm (>120), and z_min=-39.87mm (<0).
R3: FAIL - 1186 points of intersection detected with phone volume.
R4: PASS - Material found in specified region [a:90-110, b:-2-0, |y|<=15].
R5: PASS - Seat and Lip volumes confirmed via sampling.
R6: PASS - Combined COM projects inside footprint with >5mm margin.
R7: FAIL - Mass is 663.77g (>60g limit).

## Problems
- Mass: Current mass is 663.77 g; must be <= 60 g.
- Phone Interference: Stand intersects phone volume at 1186 points; must have zero intersection.
- Dimensions/Placement: x_ext is 153.46 mm (max 100), z_ext is 239.87 mm (max 120), and z_min is -39.87 mm (min 0).

SIM_CODE_ISSUE: no