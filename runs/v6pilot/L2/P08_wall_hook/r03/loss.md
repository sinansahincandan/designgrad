## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - Vol ratio 0.98 in required range [0,2]x[-8,8]x[-5,45].
R3: FAIL - Thickness around holes is less than 4 mm (thickness_ratio 0.94).
R4: FAIL - Pocket/bed geometry does not match requirements (values 0.143, 0.583).
R5: FAIL - Lip volume intersection is only 0.8.
R6: PASS - Stress 2.06 MPa $\le$ 25 MPa; Deflection 0.023 mm $\le$ 1.5 mm.
R7: PASS - Mass and X-extent are within limits.

## Problems
- Strap Seat (R4): The pocket emptiness and bed solidity do not meet the specified dimensions for $x \in [35, 45]$ and $z = -14$.
- Back Plate (R2/R3): The plate thickness around screw holes is $< 4\text{ mm}$ and does not strictly adhere to the $0 \le x \le 2$ boundary.
- Retaining Lip (R5): The lip volume is incomplete (0.8 intersection ratio).

SIM_CODE_ISSUE: no