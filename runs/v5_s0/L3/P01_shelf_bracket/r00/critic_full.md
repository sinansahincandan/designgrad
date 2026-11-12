## Working
- R1: PASS. Evidence shows 1 solid.
- R2: FAIL. BBox x-max is 150, but requirement R4 requires shelf support to reach at least x=150 and the design says arm extends to x=160. More importantly, the measured y-range [0.0, 30.0] does not center on y=0 (it should be [-20, 20] or similar).
- R3: UNSURE. Simulation was judged not faithful; visual evidence shows holes are offset from y=0.
- R4: FAIL. Shelf presence check returned False. The design claims a top surface at z=110, but the simulation fails to find material there.
- R5: UNSURE. Simulation calculation of I is physically impossible/incorrect.
- R6: UNSURE. Simulation calculation of I is physically impossible/incorrect.
- R7: FAIL. Measured mass is 119.34 g, which exceeds the limit of 90 g.

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