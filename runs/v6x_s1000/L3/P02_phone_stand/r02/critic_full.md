## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The x-extent is 120.36 mm, which exceeds the maximum allowed footprint of 100 mm. Height (75.19 mm) and min z (0.0) are fine.
- R3: FAIL. Simulation found 140 intersection points with the phone volume.
- R4: FAIL. Simulation sampled the required region ($a \in [90, 110], b \in [-2, 0]$) and found no material (value=0.0). The back support is missing or misplaced.
- R5: FAIL. Simulation sampled the seat and lip regions and found no material (value=0.0). The cradle/lip features are missing or misplaced.
- R6: PASS. Combined COM x = -27.53 is within the footprint $x \in [-95.18, 25.18]$ with a margin $> 5$ mm ($25.18 - (-27.53) = 52.71$; $-27.53 - (-95.18) = 67.65$).
- R7: FAIL. Measured mass is 89.59 g, which exceeds the limit of 60 g.

## Verdicts
R1: PASS - Counted 1 solid.
R2: FAIL - X-extent is 120.36 mm, exceeding 100 mm limit.
R3: FAIL - 140 intersection points detected with phone volume.
R4: FAIL - No material found in the specified back support region.
R5: FAIL - No material found in the specified seat and lip regions.
R6: PASS - Combined COM projects within footprint with > 5 mm margin.
R7: FAIL - Mass is 89.59 g, exceeding 60 g limit.

## Problems
- Back Support (R4): Missing/misplaced; material found = 0.0 in required region.
- Seat and Lip (R5): Missing/misplaced; material found = 0.0 in required region.
- Mass (R7): 89.59 g, exceeds limit of 60 g.
- Footprint (R2): X-extent is 120.36 mm, exceeds limit of 100 mm.
- Intersection (R3): 140 points of intersection with phone volume.

SIM_CODE_ISSUE: no