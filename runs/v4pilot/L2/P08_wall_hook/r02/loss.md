R1: PASS - Found 1 solids.
R2: PASS - Back plate covers required region with 98% fill.
R3: FAIL - Probing hole locations showed absence of material in hole volumes (holes were not successfully subtracted).
R4: FAIL - Intersection volume of bed region and pocket region is [112.0, 120.0], which contradicts the requirement for an empty space (should be 0).
R5: PASS - Lip intersection volume matches expected geometry.
R6: PASS - Bending stress 0.84 MPa <= 25 MPa; deflection 0.01 mm <= 1.5 mm.
R7: FAIL - Mass is 31.99 g, which exceeds the limit of 25 g.

Most important problems to fix:
- R7: Mass is 31.99 g (limit 25 g).
- R4: Strap pocket is not empty; intersection volume with bed region is [112.0, 120.0] instead of 0.
- R3: Screw holes are not present in the solid (material found where voids should be).

SIM_CODE_ISSUE: no