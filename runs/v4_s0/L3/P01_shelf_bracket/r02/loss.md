R1: PASS - Found 1 solid.
R2: FAIL - Bounding box Z-range is [-55, 55], violating requirement 0 <= z <= 130.
R3: FAIL - Screw holes and screwdriver clearance are missing or incorrectly placed according to simulation/render evidence.
R4: UNSURE - Simulation check errored; render shows top surface at z ≈ 55 instead of z = 110.
R5: PASS - Measured stress is 0.368 MPa, which is <= 20 MPa.
R6: PASS - Measured deflection is 0.012 mm, which is <= 2.0 mm.
R7: PASS - Measured mass is 87.26 g, which is <= 90 g.

Most important problems to fix:
- Z-axis positioning: The part's Z-range is [-55, 55]; it must be shifted so the minimum Z is 0 and the top surface is at z = 110.
- Screw holes/Clearance: R3 features (diameter 5.5 mm holes and 8x8 mm clearance) are missing or incorrectly implemented in the geometry.
- Shelf support height: The top surface is at z ≈ 55; it must be at exactly z = 110.

SIM_CODE_ISSUE: yes