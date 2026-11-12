## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured x-extent is 150 mm, which exceeds the limit of 100 mm. Height is 120 mm (at limit). Min Z is 0.
- R3: FAIL. Simulation found 3760 intersection points within the phone volume.
- R4: PASS. Volume density in the specified region is 1.0.
- R5: PASS. Seat and lip regions are fully occupied as required.
- R6: PASS. Combined COM x = -34.52. Footprint x range is [-110, 40]. The margin to the edge (x=-110) is ~75 mm, which is > 5 mm.
- R7: FAIL. Measured mass is 2008.8 g, which significantly exceeds the 60 g limit. Note: The simulation reports a volume of $1,620,000 \text{ mm}^3$, which is massive for this scale and explains the weight failure.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - x-extent is 150 mm (limit 100 mm).
R3: FAIL - 3760 intersection points detected.
R4: PASS - Volume density in region is 1.0.
R5: PASS - Seat and lip regions are fully occupied.
R6: PASS - COM projects within footprint with > 5 mm margin.
R7: FAIL - Mass is 2008.8 g (limit 60 g).

## Problems
- Mass: Current mass is 2008.8 g; must be $\le$ 60 g.
- Footprint: x-extent is 150 mm; must be $\le$ 100 mm.
- Intersection: Stand intersects phone volume at 3760 points.

SIM_CODE_ISSUE: no