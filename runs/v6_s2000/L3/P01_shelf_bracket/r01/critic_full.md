## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Bounding box Z max is 135.0 mm, which exceeds the limit of 130 mm. (Note: X max is 150, which is within 170).
- R3: FAIL. Simulation indicates failure in screwdriver clearance/hole verification for $x \ge 10$.
- R4: FAIL. The volume above $z=110$ for $x \ge 8$ is measured at $18260.0\text{ mm}^3$, violating the "nothing above $z=110$" rule. Also, the fill fraction in the support zone is only 0.4, which might not satisfy the "solid material" requirement depending on interpretation, but the height violation is definitive.
- R5: PASS. $\sigma = 0.277\text{ MPa} \le 20\text{ MPa}$.
- R6: PASS. Deflection $0.009\text{ mm} \le 2.0\text{ mm}$.
- R7: FAIL. Mass is $187.68\text{ g}$, which exceeds the limit of $90\text{ g}$.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Z max is 135.0 mm, exceeding 130 mm.
R3: FAIL - Screwdriver clearance/hole verification failed for $x \ge 10$.
R4: FAIL - Volume of $18260.0\text{ mm}^3$ exists above $z=110$ for $x \ge 8$.
R5: PASS - Stress is 0.277 MPa.
R6: PASS - Deflection is 0.009 mm.
R7: FAIL - Mass is 187.68 g, exceeding 90 g.

## Problems
- Mass: Current mass is 187.68 g; must be $\le 90\text{ g}$.
- Height Violation: Part extends to $z=135$; nothing above $z=110$ for $x \ge 8$.
- Envelope: Z max is 135 mm; must be $\le 130\text{ mm}$.
- Screw Access: Clearance channels/holes do not meet R3 requirements for $x \ge 10$.

SIM_CODE_ISSUE: no