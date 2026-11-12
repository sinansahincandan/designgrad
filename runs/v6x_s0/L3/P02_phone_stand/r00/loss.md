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