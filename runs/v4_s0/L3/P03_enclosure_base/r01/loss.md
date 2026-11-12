R1: PASS - 1 solid found.
R2: PASS - Fill ratio of 1.0 in floor region [-40,40]x[-25,25]x[0,2].
R3: PASS - Intersection volume with board space is 0.0.
R4: PASS - Bounding box [85.0, 55.0, 31.0] meets specs.
R5: FAIL - Bosses failed volume/clearance checks; render shows 0 cylindrical faces (bosses missing).
R6: FAIL - Intersection volume with cutout box is ~135 mm³, indicating the cutout was not successfully subtracted or is incorrectly sized/placed.
R7: PASS - Mass is 45.787 g, which is <= 70 g.

Most important problems to fix:
- R5: Screw bosses are missing from the geometry (n_cylindrical_faces = 0).
- R6: USB-C cutout is not correctly implemented/subtracted (intersection volume ~135 mm³ instead of 0).

SIM_CODE_ISSUE: no