## Working
- R1: FAIL. Simulation reports 2 solids; visual review confirms it is not a single manifold body.
- R2: PASS. Back plate dimensions and position are verified by intersection volume and bbox check.
- R3: FAIL. Visual review shows holes are at the wrong Z coordinates (one near z=20 instead of 0 and 40) and only one hole is visible. Simulation evidence for R3 is unreliable due to flawed detection logic.
- R4: FAIL. Bed volume probe and pocket volume probe both returned 0.0, meaning the strap seat/pocket geometry was not successfully created or measured.
- R5: PASS. Intersection volume confirms material exists in the lip region.
- R6: PASS. Simulation values for stress (0.27 MPa) and deflection (0.0007 mm) are well within limits (25 MPa, 1.5 mm).
- R7: PASS. Mass (14.43 g) is $\le$ 25 g and X extent (52 mm) is $\le$ 55 mm.

## Verdicts
R1: FAIL - Simulation reports 2 solids instead of 1.
R2: PASS - Verified by intersection volume and bbox check.
R3: FAIL - Visual review shows incorrect Z coordinates and missing second hole.
R4: FAIL - Bed and pocket volumes measured as 0.0.
R5: PASS - Verified by intersection volume.
R6: PASS - Stress and deflection are within limits.
R7: PASS - Mass and X extent are within limits.

## Problems
- R1: Entire part; contains 2 solids instead of 1 single solid.
- R3: Screw holes; located at incorrect Z coordinates (one near z=20) and only one hole exists instead of two.
- R4: Strap seat; bed volume and pocket volume are 0.0, indicating the feature is missing or incorrectly modeled.

SIM_CODE_ISSUE: yes