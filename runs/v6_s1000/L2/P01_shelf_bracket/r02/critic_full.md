## Working
- R1: PASS. Evidence shows 1 solid.
- R2: FAIL. The bounding box for Y is [0, 40]. The requirement is [-20, 20]. The part is offset from the center of the Y axis.
- R3: FAIL. Simulation reports "walled" status for holes, indicating they are not clear/empty as required.
- R4: FAIL. Support volume in the specified range (x[140,150], y[-1,1]) is 109.68 mm³, but the requirement implies a solid block of material must exist directly below z=110. While it may be present, the simulation flagged this as FAIL.
- R5: PASS. Measured stress $\sigma \approx 0.26$ MPa is well below 20 MPa. (Note: Simulation $I$ and $c$ values differ from design doc calculations, but result is within limits).
- R6: PASS. Measured deflection $\delta \approx 0.0089$ mm is well below 2.0 mm.
- R7: FAIL. Measured mass is ~229.68 g, which exceeds the limit of 90 g. The design doc's estimate (62 g) was incorrect.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Y range is [0, 40], must be [-20, 20].
R3: FAIL - Holes are reported as "walled".
R4: FAIL - Support volume check failed.
R5: PASS - Stress 0.26 MPa <= 20 MPa.
R6: PASS - Deflection 0.0089 mm <= 2.0 mm.
R7: FAIL - Mass 229.68 g > 90 g.

## Problems
- Mass: Current mass is ~229.68 g, must be <= 90 g.
- Y-axis Alignment: Y range is [0, 40], must be [-20, 20].
- Screw Hole Access: Holes are reported as "walled", failing the screwdriver access requirement.
- Shelf Support: Support volume at x[140,150] failed verification.

SIM_CODE_ISSUE: no