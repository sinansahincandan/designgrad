## Working
- R1: Evidence shows 1 solid. PASS.
- R2: Intersection with [0,2]x[-8,8]x[-5,45] yields 98% volume ratio. This indicates the plate is mostly present in the required zone. PASS.
- R3: Simulation probed holes at (0,0) and (0,40). The `thickness_ratio` was measured at ~0.69. The requirement states the plate must be "at least 4 mm thick around them". Since the plate is defined in the design as only 2mm thick ($x \in [0,2]$), it is physically impossible to have 4mm of material thickness around a hole passing through it. FAIL.
- R4: Simulation confirms pocket emptiness and bed solidity at specified coordinates. PASS.
- R5: Intersection with lip box shows presence of material. PASS.
- R6: Bending stress (1.67 MPa) is < 25 MPa; deflection (0.017 mm) is < 1.5 mm. PASS.
- R7: Mass (18.29 g) is < 25 g; X-extent (52.5 mm) is < 55 mm. PASS.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Plate geometry matches specification.
R3: FAIL - Thickness ratio 0.69 indicates material thickness around holes is insufficient; plate is only 2mm thick, but 4mm is required.
R4: PASS - Pocket and bed dimensions verified.
R5: PASS - Lip geometry verified.
R6: PASS - Stress (1.67 MPa) and deflection (0.017 mm) are within limits.
R7: PASS - Mass (18.29 g) and X-extent (52.5 mm) are within limits.

## Problems
R3: Back plate thickness is 2 mm; must be at least 4 mm thick around the screw holes.

SIM_CODE_ISSUE: no