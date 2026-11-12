## Working
- R1: Evidence shows 1 solid. PASS.
- R2: Evidence confirms annulus volume exists around bore in y=[0,4]. PASS.
- R3: Evidence confirms bore is empty (0.0 material). PASS.
- R4: Specification requires holes at $z = 30 \pm 15.5$ (i.e., $z=14.5$ and $z=45.5$). The Design Document states the holes are placed at $(x, z) = (15.5, 45.5), (15.5, 14.5), (-15.5, 45.5),$ and $(-15.5, 14.5)$. However, the simulation evidence reports a measured diameter of $0.0$ for these holes. This indicates the holes were not successfully subtracted or do not exist in the geometry. FAIL.
- R5: Evidence shows intersection volume with clearance box is 0.0. PASS.
- R6: Specification requires two vertical screw holes at $(x, y) = (\pm 25, 25)$ with diameter $5.5$ mm. The simulation reports a measured diameter of $[0.0, 0.2]$. This indicates the holes are missing or significantly undersized. FAIL.
- R7: BBox and mass (26.24g) are within limits ($x \in [-35, 35]$, $z_{max} \le 55$, mass $\le 60$g). PASS.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Annulus volume verified in y=[0,4].
R3: PASS - Bore diameter and axis verified.
R4: FAIL - Measured hole diameter is 0.0 mm; should be 3.4 mm.
R5: PASS - Clearance volume intersection is 0.0.
R6: FAIL - Measured hole diameter is [0.0, 0.2] mm; should be 5.5 mm.
R7: PASS - Envelope and mass within limits.

## Problems
- Motor screw holes: Diameter is 0.0 mm, should be 3.4 mm.
- Base mounting holes: Diameter is ~0.1 mm, should be 5.5 mm.

SIM_CODE_ISSUE: no