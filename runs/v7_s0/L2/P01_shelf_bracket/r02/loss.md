## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Bounding box within limits.
R3: FAIL - Holes at (y=0, z=20) and (y=0, z=60) are not detected in the geometry.
R4: FAIL - Fill fraction at x[140,150], y[-1,1], z[108,110] is 0.50; must be 1.0 for solid support.
R5: PASS - Stress 0.55 MPa <= 20 MPa.
R6: PASS - Deflection 0.02 mm <= 2.0 mm.
R7: PASS - Mass 76.09 g <= 90 g.

## Problems
1. Screw Holes: The cylindrical voids at (y=0, z=20) and (y=0, z=60) are missing from the geometry.
2. Shelf Support: The material between $x=140$ and $x=150$ below $z=110$ is only 50% solid; it must be a continuous solid to support the shelf.

SIM_CODE_ISSUE: no