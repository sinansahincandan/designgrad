## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - y range [0, 30] does not fit within [-20, 20].
R3: UNSURE - simulation probe errored.
R4: FAIL - fill fraction of 0.5 at x[140, 150] means the shelf is not fully supported by solid material.
R5: PASS - 0.38 MPa <= 20 MPa.
R6: PASS - 0.01 mm <= 2.0 mm.
R7: FAIL - 119.34 g > 90 g.

## Problems
- Mass: Current mass is 119.34 g, must be <= 90 g.
- Shelf Support: Fill fraction at x[140, 150] is 0.5, must be 1.0 (solid material).
- Envelope: y range is [0, 30], must be within [-20, 20].

SIM_CODE_ISSUE: yes