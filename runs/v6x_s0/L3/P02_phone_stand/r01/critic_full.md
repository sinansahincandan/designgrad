## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured x_ext is 101.76 mm, which exceeds the 100 mm limit. The reviewer also notes the footprint deviates from the design doc, but the measured value is the definitive proof of failure against the spec.
- R3: FAIL. Simulation shows an intersection volume of 219.0 units with the phone volume.
- R4: PASS. Volume fraction sampling confirms material exists in the specified region.
- R5: PASS. Volume fraction sampling confirms seat and lip regions are occupied.
- R6: PASS. Combined COM is at x = -27.6. The footprint x-range is [-56.8, 45.0]. The margin to the edge (x=-56.8) is $|-27.6 - (-56.8)| = 29.2$ mm, and to the other edge (x=45) is $45 - (-27.6) = 72.6$ mm. Both are $> 5$ mm.
- R7: PASS. Mass is 57.33 g, which is $\le 60$ g.

## Verdicts
R1: PASS - 1 solid detected.
R2: FAIL - x_ext is 101.76 mm, exceeding the 100 mm limit.
R3: FAIL - Intersection volume with phone is 219.0.
R4: PASS - Material present in specified region.
R5: PASS - Material present in seat and lip regions.
R6: PASS - Combined COM projects within footprint with $>5$ mm margin.
R7: PASS - Mass is 57.33 g, which is $\le 60$ g.

## Problems
- Phone Interference: The stand intersects the phone volume (219.0 units).
- Footprint Size: The x-extent is 101.76 mm, exceeding the 100 mm limit.

SIM_CODE_ISSUE: no