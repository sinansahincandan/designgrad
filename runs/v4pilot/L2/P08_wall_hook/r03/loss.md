R1: PASS - Found 1 solids.
R2: PASS - Bbox check and intersection volume confirm plate at $x \in [0, 2], |y| \le 8, z \in [-5, 45]$.
R3: FAIL - Probing hole locations showed no absence of material (value=0.0).
R4: FAIL - Intersection volume of bed and pocket is 112.0 mm³, meaning the "empty" space contains solid material; it should be 0.
R5: PASS - Intersection volume confirms lip at $x \in [47, 52], |y| \le 4, z \in [-13, -8]$.
R6: PASS - Bending stress 2.34 MPa ($\le$ 25) and deflection 0.02 mm ($\le$ 1.5).
R7: PASS - Mass 13.48 g ($\le$ 25 g) and X extent 52 mm ($\le$ 55 mm).

Most important problems to fix:
- Strap seat (R4): The pocket volume ($x \in [35, 45], |y| \le 6, z \in [-13, -6]$) contains 112.0 mm³ of solid material instead of being empty.
- Screw holes (R3): No material was removed at $(y,z) = (0,0)$ and $(0,40)$; the holes are not present in the geometry.

SIM_CODE_ISSUE: no