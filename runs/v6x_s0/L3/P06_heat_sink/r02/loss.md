## Verdicts
R1: PASS - Simulation confirms a single solid.
R2: PASS - BBox shows dimensions are $40 \times 40 \times 22$ mm and centered.
R3: PASS - Base volume matches the expected thickness and footprint minus holes.
R4: PASS - Measured thermal resistance is $7.218 \text{ K/W}$.
R5: FAIL - Clearance voids are misaligned (measured at $\pm 13.49, \pm 2.5$ instead of $\pm 15, 0$) and simulation shows no clearance volume was successfully created.
R6: PASS - Measured mass is $44.61\text{g}$.

## Problems
- Mounting/Clearance: The cylindrical clearance voids are located at $(\pm 13.49, \pm 2.5)$ instead of $(\pm 15, 0)$.
- Mounting/Clearance: The screwdriver clearance (voids for $z \ge 3$) is missing or incorrectly implemented as evidenced by `clearance_vol: 0.0`.

SIM_CODE_ISSUE: yes