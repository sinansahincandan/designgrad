## Working
- R1: The simulation confirms 1 solid. PASS.
- R2: Measured x_ext = 137.6 mm (> 100), z_ext = 133.5 mm (> 120), and z_min = -28.5 mm (< 0). FAIL.
- R3: Point-in-mesh sampling shows an intersection volume of 336.0 units. FAIL.
- R4: Volume fraction sampling confirms material exists in the specified rear support region. PASS.
- R5: Sampling for seat and lip regions returned [0.40625, 0.0], indicating the required geometry is missing or insufficient. FAIL.
- R6: The combined COM projection [-28.57, -2.13] falls within the footprint x[-68.8, 68.8], y[-25.0, 25.0]. PASS.
- R7: Measured mass is 140.62 g (> 60 g). FAIL.

## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: FAIL - x_ext=137.6mm (>100), z_ext=133.5mm (>120), and z_min=-28.5mm (<0).
R3: FAIL - Intersection volume of 336.0 detected.
R4: PASS - Material found in specified rear support region.
R5: FAIL - Volume fraction sampling shows seat/lip regions are not populated.
R6: PASS - Combined COM projects within footprint with margin.
R7: FAIL - Mass is 140.62g (>60g).

## Problems
- R2 (Size/Placement): x_ext=137.6mm (limit 100), z_ext=133.5mm (limit 120), z_min=-28.5mm (limit 0).
- R7 (Mass): Mass is 140.62g (limit 60g).
- R3 (Interference): Stand intersects phone volume by 336.0 units.
- R5 (Seat/Lip): Required material for seat and lip is missing.

SIM_CODE_ISSUE: no