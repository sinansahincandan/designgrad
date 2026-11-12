## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms material integrity in the face plate region.
- R3: PASS. Simulation confirms diameter is 22.5 mm on axis.
- R4: FAIL. Simulation probe at (+-15.5, 30 +- 15.5) failed to find holes. The design document lists coordinates (x=15.5, z=45.5), etc., which match the requirement, but the simulation confirms they are not present in the geometry.
- R5: PASS. Simulation confirms zero intersection with the clearance volume.
- R6: FAIL. Simulation probe shows holes do not exist (empty ratio 0.0). The visual reviewer also notes the base plate appears solid in Top/Right views and that the vertical screw holes are missing.
- R7: PASS. BBox is within limits (-35 to 35, max z=50) and mass (36.91g) is < 60g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Simulation confirms thickness and material integrity.
R3: PASS - Simulation confirms diameter and axis.
R4: FAIL - Simulation probe failed to find holes at specified coordinates.
R5: PASS - Simulation confirms clearance volume is empty.
R6: FAIL - Simulation and visual inspection confirm 5.5 mm holes are missing.
R7: PASS - BBox and mass are within limits.

## Problems
- R6: Base screw holes (diameter 5.5 mm) at (x, y) = (+-25, 25) are missing.
- R4: Motor screw holes (diameter 3.4 mm) at (x, z) = (+-15.5, 30 +- 15.5) are missing.

SIM_CODE_ISSUE: no