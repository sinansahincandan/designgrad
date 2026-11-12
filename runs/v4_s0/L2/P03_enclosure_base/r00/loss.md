R1: PASS - 1 solid found.
R2: PASS - Intersection volume of floor region (80x50x2) is 8000.0 mm3.
R3: PASS - Intersection volume with board cavity is 0.0 mm3.
R4: PASS - Bounding box [85.0, 55.0, 31.0] meets requirements.
R5: FAIL - Verified 4 bosses: OD (vol check), Hole Diameter (empty cylinder r=1.1), and Depth (empty cylinder z=4-8) returned value 0.
R6: PASS - Intersection volume with cutout probe box is 0.0 mm3.
R7: PASS - Mass is 65.47 g, which is <= 70 g.

Most important problems to fix:
- Screw Bosses (R5): The simulation failed to verify the existence/properties of the four bosses at $(\pm35, \pm20)$.

SIM_CODE_ISSUE: no