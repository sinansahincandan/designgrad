## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured x-extent is 147.54 mm (> 100), height is 178.21 mm (> 120), and min z is -5.0 (< 0).
- R3: FAIL. Simulation found 160 intersection points with the phone volume.
- R4: PASS. Material exists in the specified region (a=100, b=[-2,0]).
- R5: FAIL. Simulation shows no material in the seat/lip regions (values are near zero).
- R6: PASS. Combined COM x = -27.79 is within footprint [-98.53, 49.02]. Note: The reviewer's claim of a 3.64 mm margin contradicts the simulation evidence which states the projection is well within the footprint (margin calculation: distance from -27.79 to edge at -98.53 is ~70mm; distance to edge at 49.02 is ~76mm). However, R6 is PASS based on the provided simulation data.
- R7: FAIL. Measured mass is 114.78 g (> 60 g).

## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: FAIL - x-extent 147.54 mm > 100 mm, height 178.21 mm > 120 mm, min z -5.0 < 0.
R3: FAIL - 160 intersection points detected.
R4: PASS - Material found in specified region.
R5: FAIL - No material found in seat or lip regions.
R6: PASS - Combined COM projects inside footprint.
R7: FAIL - Mass 114.78 g > 60 g.

## Problems
- Footprint/Height: X extent is 147.54 mm (limit 100), Height is 178.21 mm (limit 120), Min Z is -5.0 (limit 0).
- Mass: Measured mass is 114.78 g (limit 60 g).
- Intersection: Stand intersects phone volume at 160 points.
- Seat/Lip: No material present in the required seat and lip regions.

SIM_CODE_ISSUE: no