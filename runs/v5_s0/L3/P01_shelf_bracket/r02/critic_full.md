## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The BBox shows y ranges from [0, 40]. Requirement is [-20, 20]. The part is offset along the Y axis.
- R3: PASS. Simulation confirms holes and clearance are present. (Note: Reviewer render claim of missing holes contradicts simulation evidence; I rely on simulation).
- R4: PASS. Simulation confirms shelf at z=110 and no material above for x>=8.
- R5: PASS. Measured stress 0.26 MPa <= 20 MPa.
- R6: PASS. Measured deflection 0.01 mm <= 2.0 mm.
- R7: FAIL. Measured mass is 170.50 g, which exceeds the limit of 90 g.

## Verdicts
R1: PASS - Simulation confirms one solid.
R2: FAIL - Y-envelope is [0, 40], must be [-20, 20].
R3: PASS - Simulation verifies hole diameter and clearance.
R4: PASS - Simulation verifies shelf height and top clearance.
R5: PASS - Measured stress 0.26 MPa <= 20 MPa.
R6: PASS - Measured deflection 0.01 mm <= 2.0 mm.
R7: FAIL - Measured mass 170.50 g > 90 g.

## Problems
- Mass (R7): Value is 170.50 g, should be <= 90 g.
- Y-Envelope (R2): Y-range is [0, 40], should be [-20, 20].

SIM_CODE_ISSUE: no