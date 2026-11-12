## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Simulation shows no material at $y=4$ in the ring around the bore. This implies the face plate is either too thin or the subtraction for the bore/holes has removed all material.
- R3: FAIL. The simulation reports a "walled_ratio" of 0.359 and an "empty_ratio" of 0.026, which indicates the central bore is not actually an empty hole through the plate as required.
- R4: FAIL. Simulation shows zero cylinders found at the specified $(x, z)$ coordinates for the motor screw holes.
- R5: PASS. Intersection volume with clearance box is $0.0\text{ mm}^3$.
- R6: FAIL. Simulation reports 0 holes found at $(\pm 25, 25)$. The base mounting holes are missing.
- R7: PASS. BBox and mass ($31.62\text{ g}$) are within limits ($-35 \le x \le 35$, $z_{max} \le 55$, mass $\le 60\text{ g}$).

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