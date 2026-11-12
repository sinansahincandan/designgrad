## Working
- R1: Evidence shows 1 solid. PASS.
- R2: Back plate covers $x \in [0, 4]$, which satisfies $0 \le x \le 2$ and minimum $x=0$. PASS.
- R3: Simulation reports hole volumes of 0.0. This indicates the screw holes were not successfully subtracted or do not exist as voids in the geometry. FAIL.
- R4: Bed volume is 96.0 (matches $10 \times 2 \times 4.8$ area approx) and pocket volume is 0.0 (meaning the space is empty). PASS.
- R5: Intersection volume with lip region matches expected geometry. PASS.
- R6: Stress $\sigma = Mc/I = (1600 \cdot 9.5) / 10640 \approx 1.42\text{ MPa}$ ($\le 25$). Deflection $FL^3/3EI = (50 \cdot 32^3) / (3 \cdot 3500 \cdot 10640) \approx 0.0147\text{ mm}$ ($\le 1.5$). PASS.
- R7: Mass $17.34\text{ g} \le 25\text{ g}$. X-extent $52\text{ mm} \le 55\text{ mm}$. PASS.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - Back plate dimensions and position meet requirements.
R3: FAIL - Hole volumes are 0.0, indicating screw holes are missing or not voids.
R4: PASS - Strap bed and pocket geometry verified.
R5: PASS - Retaining lip volume verified.
R6: PASS - Stress (1.43 MPa) and deflection (0.015 mm) are within limits.
R7: PASS - Mass (17.34 g) and X-extent (52 mm) are within limits.

## Problems
Screw holes: hole volumes are 0.0 mm³, should be $\approx 153.9\text{ mm}^3$ (two cylinders of $\varnothing 4.5$ through $4\text{ mm}$ plate).

SIM_CODE_ISSUE: no