R1: PASS - Counted 1 solid in STEP file.
R2: PASS - Intersected part with box [0,2]x[-8,8]x[-5,45], vol ratio=0.980.
R3: FAIL - Probed cylinders for emptiness returned value 0.0; render shows only one hole at z=20 instead of two at (0,0) and (0,40).
R4: FAIL - Pocket volume is 0.00 mm3 according to simulation, meaning no pocket was actually subtracted to create the seat.
R5: PASS - Lip fill ratio is 1.00.
R6: PASS - Bending stress 1.51 MPa <= 25 MPa and deflection 0.01 mm <= 1.5 mm.
R7: PASS - Mass 17.43 g <= 25 g; X-ext 52.0 mm <= 55 mm.

Most important problems to fix:
- R4 Strap Seat: Pocket volume is 0.00 mm3; the subtraction failed to create the required empty space (35 <= x <= 45, |y| <= 6, -13 <= z <= -6).
- R3 Screw Holes: Only one hole exists at z=20; should have two holes of diameter 4.5 mm at (y,z) = (0,0) and (0,40).

SIM_CODE_ISSUE: yes