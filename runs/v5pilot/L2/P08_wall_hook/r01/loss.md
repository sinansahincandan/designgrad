## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Intersection volume is only 94.42% of the required region.
R3: UNSURE - Simulation failed to verify material thickness around holes.
R4: PASS - Bed and pocket volumes match specification.
R5: PASS - Lip geometry matches specification.
R6: PASS - Stress (1.63 MPa) and deflection (0.017 mm) are within limits.
R7: PASS - Mass (18.12 g) and X-extent (52 mm) are within limits.

## Problems
Back Plate: The volume of the plate in the region $x \in [0, 2], |y| \le 8, z \in [-5, 45]$ is only 94.42% of required.
Screw Hole Thickness: The back plate thickness is 2 mm, which makes it impossible to satisfy the requirement for 4 mm of material around the holes (R3).

SIM_CODE_ISSUE: yes