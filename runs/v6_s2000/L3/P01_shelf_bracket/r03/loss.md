## Verdicts
R1: PASS - Counted 1 solid.
R2: FAIL - Y dimension is [0, 40], must be within [-20, 20].
R3: FAIL - Screw holes are missing or not functional (empty_ratio 0.0).
R4: FAIL - Fill fraction at $x \in [140, 150]$ is 0.5, must be solid (1.0).
R5: PASS - Stress 0.26 MPa $\le$ 20 MPa.
R6: PASS - Deflection 0.0089 mm $\le$ 2.0 mm.
R7: FAIL - Mass is 443.81 g, must be $\le$ 90 g.

## Problems
- Mass: Current mass 443.81 g, should be $\le$ 90 g.
- Y-Envelope: Current y range [0, 40], should be [-20, 20].
- Screw Holes: No holes detected (empty_ratio 0.0), must have 5.5 mm diameter holes at specified locations with clearance.
- Shelf Support: Fill fraction at $x \in [140, 150]$ is 0.5, should be 1.0 (solid).

SIM_CODE_ISSUE: no