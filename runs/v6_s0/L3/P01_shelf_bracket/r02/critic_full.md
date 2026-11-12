## Working
- R1: The simulation reports 2 solids; the visual reviewer confirms the spine and arm are disconnected. FAIL.
- R2: Bounding box shows $z_{min} = -55$, which is outside the required $0 \le z \le 130$. Also, while $x$ and $y$ ranges are within limits, the $z$ violation is definitive. FAIL.
- R3: Simulation reports `diameter_check_passed: false` and material exists within the clearance zone for $x \ge 10$. Visual reviewer notes holes are at $x=140$ instead of near the wall ($x \approx 0$). FAIL.
- R4: Simulation shows support column fill is nearly zero (0.11 mm), failing to provide solid material between $x=140$ and $150$. Visual reviewer notes the pillar is missing. FAIL.
- R5: Measured stress $\sigma = 1.13 \text{ MPa} \le 20 \text{ MPa}$. PASS.
- R6: Measured deflection $\delta = 0.038 \text{ mm} \le 2.0 \text{ mm}$. PASS.
- R7: Measured mass $31.7 \text{ g} \le 90 \text{ g}$. PASS.

## Verdicts
R1: FAIL - The part consists of two disconnected solids.
R2: FAIL - Minimum Z is -55, violating the requirement $z \ge 0$.
R3: FAIL - Screw holes are incorrectly located at $x=140$ and clearance requirements are not met.
R4: FAIL - No solid material exists below $z=110$ in the $x=[140, 150]$ range.
R5: PASS - Measured stress is 1.13 MPa.
R6: PASS - Measured deflection is 0.038 mm.
R7: PASS - Measured mass is 31.7 g.

## Problems
- Connectivity: The wall spine and trussed arm are disconnected solids; they must be a single valid solid (R1).
- Screw Hole Placement: Holes are at $x=140$; they must be centered at $y=0$ on the wall ($x \approx 0$) (R3).
- Shelf Support: The support pillar is missing or insufficient in the $x=[140, 150]$ range (R4).
- Z-Axis Alignment: Minimum Z is -55; it must be $\ge 0$ (R2).
- Screw Clearance: Material exists within 4 mm of hole axes for $x \ge 10$ (R3).

SIM_CODE_ISSUE: no