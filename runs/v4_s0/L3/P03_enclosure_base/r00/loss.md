R1: PASS - Counted 1 solid.
R2: PASS - Fill ratio of 1.0 in floor region [-40,40]x[-25,25]x[0,2].
R3: PASS - Intersection volume with board space is 0.0.
R4: PASS - Bounding box [85.0, 55.0, 31.0] meets dimensions and height requirements.
R5: PASS - Bosses at (+-35, +-20) have correct diameter and pilot hole depth (4mm).
R6: FAIL - Intersection volume with cutout box is 67.5; the cutout is missing from the geometry according to the visual render.
R7: PASS - Mass is 65.468 g, which is <= 70 g.

Most important problems to fix:
- USB-C Cutout (R6): The aperture is missing from the -X wall; it must be a void of at least 9mm (Y) x 3mm (Z).
- Screw Bosses (R5): Visual evidence suggests bosses are submerged or incorrectly modeled, despite simulation passing.

SIM_CODE_ISSUE: no