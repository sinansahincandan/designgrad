## Working
- R1: PASS. Evidence shows 1 solid.
- R2: PASS. Bounding box [0, 150] x [-20, 20] x [0, 110] is within the required limits [0, 170] x [-20, 20] x [0, 130].
- R3: FAIL. The simulation evidence for screw holes shows `empty_ratio: 0.0` and `clearance_vol: 0`. This indicates that the boolean subtractions for the screw holes (diameter 5.5mm) and the clearance channels (radius 4mm) failed to actually remove material from the solid, or the geometry does not contain these voids at the specified locations.
- R4: PASS. Fill fraction is 1.0 in the support zone [140, 150] and no material exists above z=110 for x>=8.
- R5: PASS. $\sigma = 1.37 \text{ MPa} \le 20 \text{ MPa}$.
- R6: PASS. $\delta = 0.0377 \text{ mm} \le 2.0 \text{ mm}$.
- R7: PASS. Mass is $54.83 \text{ g} \le 90 \text{ g}$.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Simulation shows no volume removed for screw holes or clearance channels (empty_ratio=0).
R4: PASS - Fill fraction 1.0 at tip and no material above z=110 for x>=8.
R5: PASS - Stress 1.37 MPa <= 20 MPa.
R6: PASS - Deflection 0.0377 mm <= 2.0 mm.
R7: PASS - Mass 54.83 g <= 90 g.

## Problems
Screw holes and clearance channels: The simulation shows no material was removed for the screw axes or the screwdriver access channels (clearance_vol = 0).

SIM_CODE_ISSUE: no