R1: PASS - Counted 1 solid in STEP file.
R2: PASS - Intersection with box [0,2]x[-8,8]x[-5,45] shows vol ratio ~0.98.
R3: FAIL - Simulation probe for holes at (0,0) and (0,40) returned 0.0; visual evidence shows only one hole or incorrect placement at z=20.
R4: PASS - Bed top is at z=-14 and pocket volume is 0.00 mm3 (implying the subtraction was successful/empty).
R5: PASS - Lip fill ratio is 1.0.
R6: PASS - Bending stress 3.03 MPa <= 25 MPa; deflection 0.04 mm <= 1.5 mm.
R7: PASS - Mass 16.77 g <= 25 g; X extent 52.0 mm <= 55 mm.

Most important problems to fix:
- Screw holes (R3): The hole at (y,z) = (0,40) is missing or incorrectly placed at z=20.
- Screw holes (R3): The simulation failed to find the required cylindrical voids for both specified holes.

SIM_CODE_ISSUE: yes