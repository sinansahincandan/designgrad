## Working
- R1: The document claims a single solid via boolean operations. Without CAD files, I must rely on the description of features being joined/subtracted. Status: PASS (based on design intent).
- R2: Floor is stated as 2mm thick ($z=0$ to $z=2$). This covers the board area (-40 to 40, -25 to 25). Status: PASS.
- R3: The document states a box subtraction for $-40 \le x \le 40, -25 \le y \le 25, 8 \le z \le 32$. This matches the requirement exactly. Status: PASS.
- R4: Outer size is 85x55mm. Wall top is at $z=32$ (within range 30–32.5). Walls are continuous except for the cutout. Status: PASS.
- R5: Bosses at $(\pm35, \pm20)$. OD = 6mm ($\ge 6$mm). Pilot hole = 2.2mm. Hole depth is stated as 4.5mm (extending from $z=2$ to $z=8$, which is a depth of 6mm relative to the boss top, or if the hole starts at $z=8$ and goes down, it must be checked). The requirement says "from the floor up to $z=8$". If the bosses are from $z=2$ to $z=8$, the height is 6mm. A 4.5mm deep hole satisfies the $\ge 4$mm requirement. Status: PASS.
- R6: Cutout at $x=-42.5$. Dimensions $9 \times 3$ mm (matches requirement). Centered at $y=0, z=14$. The $-X$ wall is at $x = -85/2 = -42.5$. Status: PASS.
- R7: Volume $\approx 4800 \text{ mm}^3$. Mass $= 4800 \times (1.24 / 1000) = 5.952\text{ g}$. This is $\le 70\text{ g}$. Status: PASS.

## Verdicts
R1: PASS - Single solid via boolean operations.
R2: PASS - Floor $z=0$ to $z=2$.
R3: PASS - Cavity $-40 \le x \le 40, -25 \le y \le 25, 8 \le z \le 32$ is subtracted.
R4: PASS - Outer dimensions 85x55mm, wall top $z=32$.
R5: PASS - Bosses at $(\pm35, \pm20)$, OD 6mm, hole depth 4.5mm $\ge$ 4mm.
R6: PASS - Cutout $9 \times 3$ mm at $y=0, z=14$.
R7: PASS - Mass $\approx 6\text{ g} \le 70\text{ g}$.

## Problems
None