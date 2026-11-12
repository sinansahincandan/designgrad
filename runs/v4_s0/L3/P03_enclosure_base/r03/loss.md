R1: PASS - Counted 1 solid.
R2: PASS - Fill ratio of 1.0 in region [-40,40]x[-25,25]x[0,2].
R3: PASS - Intersection volume with board space is 0.0.
R4: PASS - Bounding box [85.0, 55.0, 31.0] meets specs.
R5: PASS - Bosses at (+-35, +-20) verified for OD and pilot hole depth.
R6: FAIL - Intersection volume with cutout box is 67.5 mm³, which is not zero (the cutout must be empty space).
R7: PASS - Mass is 65.468 g, which is <= 70 g.

Most important problems to fix:
- USB-C Cutout (R6): The simulation shows material exists where the cutout should be (intersection volume 67.5 mm³), and the visual render shows the cutout is missing entirely.

SIM_CODE_ISSUE: no