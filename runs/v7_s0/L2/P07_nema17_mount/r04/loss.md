## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Material presence check at $y=4$ failed.
R3: FAIL - Bore is not an empty hole (empty_ratio 0.026).
R4: FAIL - Motor screw holes were not found at specified coordinates.
R5: PASS - No material in clearance volume.
R6: FAIL - Base mounting holes were not found.
R7: PASS - Envelope and mass are within limits.

## Problems
- R3/R4/R6: Missing or incorrectly implemented holes; the subtraction operations for the central bore, motor screw holes, and base screw holes failed to create empty space.
- R2: Face plate geometry is invalid; material is missing at $y=4$ around the bore.

SIM_CODE_ISSUE: no