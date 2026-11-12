## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box y range is [0, 40]. Requirement specifies -20 <= y <= 20. The part is offset from the wall centerline.
- R3: FAIL. Simulation reports `clear: false` for the screwdriver access requirement (no material within 4mm of hole axis for x >= 10).
- R4: FAIL. Simulation shows a fill ratio of 0.5 in the specified region, but the design document/render suggests the shelf support might not meet the "solid material directly below z=110 between x=140 and 150" requirement or is incorrectly positioned relative to the bounding box.
- R5: PASS. Measured stress $\sigma \approx 0.27$ MPa is well below 20 MPa.
- R6: PASS. Measured deflection $\delta \approx 0.009$ mm is well below 2.0 mm.
- R7: FAIL. Measured mass is 179.91 g, which exceeds the limit of 90 g.

## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: FAIL - y range [0, 40] does not satisfy [-20, 20].
R3: FAIL - screwdriver clearance for x >= 10 is not met.
R4: FAIL - material presence/positioning at z=110 fails check.
R5: PASS - measured stress 0.27 MPa <= 20 MPa.
R6: PASS - measured deflection 0.009 mm <= 2.0 mm.
R7: FAIL - mass 179.91 g > 90 g.

## Problems
- Mass: Current mass is 179.91 g, must be <= 90 g.
- Y-Envelope: Current y range is [0, 40], must be within [-20, 20].
- Screwdriver Access: Clearance for x >= 10 around hole axes is not provided.
- Shelf Support: Material at z=110 between x=140 and 150 does not meet specification.

SIM_CODE_ISSUE: no