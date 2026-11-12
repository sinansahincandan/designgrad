## Verdicts
R1: PASS - Evidence shows 1 solid.
R2: FAIL - BBox y-range [0, 30] does not satisfy centered requirement and x-max is insufficient for R4.
R3: UNSURE - Simulation check was judged not faithful and visual evidence suggests offset holes.
R4: FAIL - Shelf presence check returned False.
R5: UNSURE - Simulation calculation of I is physically impossible.
R6: UNSURE - Simulation calculation of I is physically impossible.
R7: FAIL - Measured mass 119.34 g > 90 g.

## Problems
- Mass: 119.34 g (should be <= 90 g).
- Shelf Support: No material detected at z=110 for x in [140, 150] (should have solid material).
- Envelope/Centering: y-range is [0, 30] (should be centered on y=0, e.g., [-15, 15]).
- Screw Holes: Centered at y != 0 (should be y=0).

SIM_CODE_ISSUE: yes