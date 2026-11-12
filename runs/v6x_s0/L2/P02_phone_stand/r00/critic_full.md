## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured x_ext=137.64 mm (> 100 mm), z_ext=133.51 mm (> 120 mm), and z_min=-28.51 mm (< 0). The stand does not sit on the desk plane correctly and exceeds all dimensions.
- R3: FAIL. Simulation shows a volume of 336.0 $mm^3$ of intersection between the stand and the phone.
- R4: PASS. Volume fraction sampling confirms material exists in the specified rear support region.
- R5: FAIL. Measured volume fraction is [0.40625, 0.0]. This indicates the "seat" part of the requirement might be met, but the "lip" (the second value) is 0.0, meaning no material exists in the specified lip region.
- R6: PASS. Combined COM projection [-28.57, -2.13] falls within the footprint x[-68.82, 68.82], y[-25.0, 25.0] with sufficient margin.
- R7: FAIL. Measured mass is 140.62 g, which exceeds the limit of 60 g.

## Verdicts
R1: PASS - Counted 1 solid.
R2: FAIL - x_ext=137.64mm (>100), z_ext=133.51mm (>120), and z_min=-28.51mm (<0).
R3: FAIL - Intersection volume is 336.0 mm3.
R4: PASS - Material found in specified rear support region.
R5: FAIL - Lip volume fraction is 0.0.
R6: PASS - Combined COM projects within footprint with margin.
R7: FAIL - Mass is 140.62g (>60g).

## Problems
- Mass: 140.62 g (should be <= 60 g).
- Dimensions: x_ext=137.64 mm, z_ext=133.51 mm, z_min=-28.51 mm (should be x<=100, z<=120, z_min=0).
- Phone Interference: 336.0 mm3 intersection (should be 0).
- Front Lip: Volume fraction 0.0 (should be > 0 in specified region).

SIM_CODE_ISSUE: no