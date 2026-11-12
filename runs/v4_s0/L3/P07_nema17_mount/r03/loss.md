R1: PASS - Counted 1 solid in STEP file.
R2: PASS - Continuity check around bore at y=[0,4] is True.
R3: PASS - Material volume inside cylinder (r=11.25) at x=0, z=30 is 0.0 mm3.
R4: FAIL - Motor screw holes are at z = 13.74 and 45.5; requirement R4 specifies z = 14.5 and 45.5 (30 +/- 15.5).
R5: PASS - Intersection volume with clearance box is 0.0.
R6: PASS - Checked z_min=0.0 and probed cylinders at (+-25, 25).
R7: FAIL - Mass is 76.13 g; requirement R7 specifies mass <= 60 g.

Most important problems to fix:
- Mass: 76.13 g (exceeds limit of 60 g).
- Motor screw hole Z-coordinates: z = 13.74 (should be 14.5).

SIM_CODE_ISSUE: no