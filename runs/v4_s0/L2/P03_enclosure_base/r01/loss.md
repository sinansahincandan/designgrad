R1: PASS - 1 solid found.
R2: PASS - Intersection volume of floor region (80x50x2 at z=0) is 8000.0 mm3.
R3: PASS - Intersection volume of board cavity region is 0.0 mm3.
R4: PASS - Bounding box [85.0, 55.0, 31.0] meets limits.
R5: FAIL - Verified 4 bosses: OD (vol check), Hole Diameter (empty cylinder r=1.1), and Depth (empty cylinder z=4-8) returned value 0.
R6: PASS - Intersection volume of cutout probe box is 0.0 mm3.
R7: PASS - Mass is 46.19 g, which is <= 70 g.

Most important problems to fix:
- Screw Bosses (R5): The simulation failed to verify the existence/properties of the four bosses; they are either missing or incorrectly modeled despite being described in the concept.

SIM_CODE_ISSUE: no