## Verdicts
R1: PASS - Evidence from simulation confirms 1 solid.
R2: PASS - Evidence from simulation confirms material at y=4 around bore.
R3: FAIL - Simulation reports a walled_ratio of 0.383 for the central bore, indicating it is not a clean through-hole.
R4: FAIL - Simulation reports 0 holes found at specified coordinates.
R5: PASS - Evidence from simulation confirms zero intersection with clearance volume.
R6: PASS - Evidence from simulation confirms min Z=0 and hole existence.
R7: PASS - Evidence from simulation confirms envelope and mass are within limits.

## Problems
Motor screw holes: 0 holes detected; should be 4 holes of diameter 3.4 mm at (+-15.5, 30 +- 15.5).
Central bore: non-zero walled_ratio (0.383) in the void; should be a clean through-hole with 0% wall ratio in the specified radius.

SIM_CODE_ISSUE: yes