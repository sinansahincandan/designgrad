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