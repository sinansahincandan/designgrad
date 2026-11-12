## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. BBox [0, 130] x [-12.5, 12.5] x [0, 14] is within limits (x $\le$ 136, |y| $\le$ 16, z $\le$ 20).
- R3: FAIL. Probing at (6, $\pm$6) for 3.2mm holes returned empty/walled ratios near zero, indicating the holes are not present or do not intersect the geometry correctly.
- R4: FAIL. Simulation probe returned `null`, indicating the motor mount holes (four 3.2mm and one 6mm shaft hole) were not found.
- R5: PASS. $\sigma = 2.73$ MPa is $\le$ 30 MPa.
- R6: PASS. $I$ at $x=20$ is measured as 3054.595, which is $\gg$ 1.0 mm$^4$. (Note: The design doc claimed $I \approx 150$, but the simulation found a much higher value; however, both satisfy R6).
- R7: PASS. Mass = 13.68 g $\le$ 20 g.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - BBox [0, 130] x [-12.5, 12.5] x [0, 14] is within limits.
R3: FAIL - Holes at (6, $\pm$6) not detected by probe.
R4: FAIL - Motor mount holes not detected by probe.
R5: PASS - Stress 2.73 MPa $\le$ 30 MPa.
R6: PASS - $I = 3054.595 \ge 1.0$.
R7: PASS - Mass 13.68 g $\le$ 20 g.

## Problems
- Motor mount holes (R4): Four 3.2mm holes and one 6mm shaft hole are missing or incorrectly placed.
- Frame attachment holes (R3): Two 3.2mm holes at (6, $\pm$6) are missing or incorrectly placed.

SIM_CODE_ISSUE: no