## Working
- R1: PASS. Evidence shows 1 solid.
- R2: FAIL. The bounding box measurement `x[-20, 20], y[-20, 20], z[0, 160]` indicates the coordinate axes are swapped or misaligned with the specification (Spec requires $x$ to be depth/thickness and $y$ to be width along wall). The measured $z$ goes up to 160, exceeding the limit of 130.
- R3: FAIL. While diameter is correct, the screwdriver clearance check failed according to simulation evidence.
- R4: FAIL. Simulation shows excess volume above $z=110$ for $x \ge 8$. The design document claims it complies, but the measured value `3057.53` indicates a violation.
- R5: PASS. Measured stress $\approx 0.26$ MPa is well below 20 MPa.
- R6: PASS. Measured deflection $\approx 0.005$ mm is well below 2.0 mm.
- R7: FAIL. Measured mass is $158.99$ g, which exceeds the limit of $90$ g.

## Verdicts
R1: PASS - Counted 1 solid.
R2: FAIL - Bounding box $z=160$ exceeds limit of 130; axes appear swapped relative to spec.
R3: FAIL - Screwdriver clearance check failed.
R4: FAIL - Measured excess volume above $z=110$ for $x \ge 8$.
R5: PASS - Stress is 0.26 MPa $\le$ 20 MPa.
R6: PASS - Deflection is 0.005 mm $\le$ 2.0 mm.
R7: FAIL - Mass is 158.99 g > 90 g.

## Problems
- Mass: Current mass is ~159g; must be $\le$ 90g.
- Envelope/Orientation: $z$-dimension reaches 160mm (limit 130mm); coordinate axes do not match specification requirements.
- Clearance: Screw hole access for $x \ge 10$ fails the 4mm clearance requirement.
- Top Surface: Material exists above $z=110$ for $x \ge 8$.

SIM_CODE_ISSUE: yes