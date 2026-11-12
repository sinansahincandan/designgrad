## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Thickness and material presence confirmed at $y=0$ and $y=4$.
- R3: FAIL. The probe shows the bore is almost entirely empty (0.39mm walled vs 22.5mm diameter required). This suggests the hole was not cut correctly or is misplaced.
- R4: FAIL. Simulation found 0/4 valid holes at the specified coordinates. The design document claims they are implemented, but the evidence shows no voids exist at those locations.
- R5: PASS. Interference volume with motor clearance box is 0.0.
- R6: FAIL. While $z_{min}$ is effectively 0, the simulation found 0/2 vertical holes of $\varnothing 5.5$ mm at $(\pm 25, 25)$.
- R7: PASS. Envelope dimensions and mass (45.4g) are within limits.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Thickness check passed.
R3: FAIL - Bore probe shows only ~0.4mm of material/void instead of a 22.5mm diameter hole.
R4: FAIL - 0 out of 4 motor screw holes were detected at the specified locations.
R5: PASS - No interference with motor clearance volume.
R6: FAIL - 0 out of 2 table mounting holes were detected.
R7: PASS - Envelope and mass are within limits.

## Problems
- Motor Screw Holes (R4): 0 holes found; 4 holes of $\varnothing 3.4$ mm required at $(\pm 15.5, 30 \pm 15.5)$.
- Central Bore (R3): Diameter is not 22.5 mm; probe shows ~0.4 mm.
- Table Mounting Holes (R6): 0 holes found; 2 holes of $\varnothing 5.5$ mm required at $(\pm 25, 25)$.

SIM_CODE_ISSUE: no