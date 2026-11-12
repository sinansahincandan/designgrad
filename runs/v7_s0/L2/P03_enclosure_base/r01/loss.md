## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor thickness and coverage verified by intersection.
R3: PASS - Cavity volume verified empty by intersection.
R4: FAIL - Wall top $z_{max}$ is 33.0, exceeding the limit of 32.5.
R5: PASS - Bosses meet all geometric and hole requirements.
R6: UNSURE - Simulation probe failed/errored; cannot verify cutout penetration.
R7: PASS - Mass is 38.22g.

## Problems
- Wall Height: Top of wall is at $z=33.0$; must be between $z=30$ and $z=32.5$.
- USB-C Cutout: Verification failed due to simulation error; ensure cutout fully penetrates the -X wall.

SIM_CODE_ISSUE: yes