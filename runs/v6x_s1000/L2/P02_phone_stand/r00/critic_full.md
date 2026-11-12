## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Extents are $x \approx 65.8$, $y=90$, $z=80$. All within limits ($100 \times 100$ footprint, $\le 120$ height). Min $z=0$.
- R3: FAIL. Simulation found 60 intersection points within the phone volume.
- R4: FAIL. Simulation sampled the required region (a[90,110], b[-2,0]) and found 0.0 material presence. The back support is missing or incorrectly placed.
- R5: FAIL. Simulation sampled seat/lip regions and found insufficient coverage (values $0.4375$ and $0.0$). This indicates the cradle does not meet the geometric requirements to prevent sliding.
- R6: PASS. Combined COM x = -27.45. Footprint x range is [-45.76, 20.0]. The margin from COM to edge is $|-27.45 - (-45.76)| = 18.31$ mm and $|-27.45 - 20| = 47.45$ mm. Both are $> 5$ mm.
- R7: PASS. Mass is $\approx 41.47$ g, which is $< 60$ g.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Extents within limits and min z=0.
R3: FAIL - 60 intersection points detected with phone volume.
R4: FAIL - No material found in the specified back support region (a[90,110], b[-2,0]).
R5: FAIL - Material coverage in seat/lip regions is insufficient or zero.
R6: PASS - COM projection margin is $> 5$ mm.
R7: PASS - Mass is $\approx 41.47$ g.

## Problems
- Intersection: The stand geometry intersects the phone volume (60 points detected).
- Back Support: No material exists in the required region $a \in [90, 110], b \in [-2, 0]$.
- Cradle/Lip: Insufficient material in seat ($a \in [-4, 0]$) and lip ($a \in [0, 8]$) regions.

SIM_CODE_ISSUE: no