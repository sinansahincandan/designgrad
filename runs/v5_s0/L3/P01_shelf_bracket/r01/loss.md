## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - y-range [0, 30] is outside required [-20, 20].
R3: UNSURE - Simulation check was unfaithful and screw holes are not detected in geometry.
R4: FAIL - No solid material exists below z=110 for x in [140, 150].
R5: PASS - 0.35 MPa <= 20 MPa.
R6: PASS - 0.01 mm <= 2.0 mm.
R7: FAIL - 112.84 g > 90 g.

## Problems
- Mass (R7): Current mass is 112.84 g, must be <= 90 g.
- Shelf Support (R4): No solid material exists below z=110 between x=140 and 150; required solid support for shelf.
- Envelope (R2): y-dimension is [0, 30], must be within [-20, 20].
- Screw Holes (R3): Screw holes are not present in the geometry/subtractions failed.

SIM_CODE_ISSUE: yes