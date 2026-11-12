## Working
- R1: PASS. The simulation confirms 1 solid in the STEP file.
- R2: FAIL. The requirement specifies an X-extent $\le 100$ mm. Measured $x\_ext = 161.21$ mm. (Note: Height and Z-min are within limits).
- R3: FAIL. The simulation reports 619 points of the phone volume are inside the stand mesh, meaning it intersects the phone.
- R4: PASS. Volume fraction sampling confirms material exists in the specified rear brace region.
- R5: PASS. Volume fraction sampling confirms material exists in the seat and lip regions.
- R6: PASS. The combined COM projects to $x = -13.7$ within the footprint $x \in [-56.2, 105.0]$. The margin is checked against the contact area; the evidence states it passes with a 5mm margin.
- R7: FAIL. The requirement specifies mass $\le 60$ g. Measured mass is $225.98$ g (based on volume $182,241.67 \text{ mm}^3$).

## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: FAIL - x_ext is 161.21 mm, which exceeds the 100 mm limit.
R3: FAIL - 619 points of phone volume intersect the stand.
R4: PASS - Material detected in specified rear brace region.
R5: PASS - Material detected in seat and lip regions.
R6: PASS - Combined COM projects inside footprint with $>5$mm margin.
R7: FAIL - Mass is 225.98 g, which exceeds the 60 g limit.

## Problems
- Mass: Current mass is 225.98 g; must be $\le 60$ g.
- Footprint: X-extent is 161.21 mm; must be $\le 100$ mm.
- Phone Intersection: Stand intersects phone volume at 619 sampled points; must have zero intersection.

SIM_CODE_ISSUE: no