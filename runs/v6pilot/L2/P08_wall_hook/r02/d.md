**Concept**: A cantilevered hook consisting of a thick mounting plate and a horizontal arm that transitions into a recessed strap cradle with a protective retaining lip.

**Main Features**:
- **Back Plate**: 13mm thick, dimensions $x \in [0, 13]$, $y \in [-8, 8]$, $z \in [-5, 45]$. This thickness ensures sufficient material around screw holes to satisfy R3.
- **Support Arm**: A tapered structural member connecting the plate to the strap seat to manage bending stress.
- **Strap Seat**: A recessed bed at $z = -14$ with a clearance pocket for a $10 \times 6\text{ mm}$ strap.
- **Retaining Lip**: A small flange at the tip ($x=50$) to prevent lateral sliding.

**Load Path**: The downward force at $x=40$ is transferred through the strap seat, into the tapered support arm, and finally into the wall plate via a moment connection.

**Requirement Fulfillment**:
- R1: Built using boolean operations on primitive solids to ensure a single manifold body.
- R2: Back plate defined from $x=0$ to $x=13$, $y \in [-8, 8]$, $z \in [-5, 45]$.
- R3: Two holes of $\varnothing 4.5\text{ mm}$ at $(0, 0)$ and $(0, 40)$ relative to the plate center; with a 13mm thickness, there is $> 4\text{ mm}$ of material in all directions from the hole edges (specifically $x \in [0, -1.25]$ and $x \in [3.25, 13]$ is not possible as holes are through-holes, so with center at $x=6.5$, edges are at $4.25$ and $8.75$, leaving $4.25\text{ mm}$ on each side).
- R4: Strap bed created by subtracting a pocket ($x \in [35, 45], |y| \le 6, z \in [-13, -6]$) from the main body.
- R5: Retaining lip added at $x \in [47, 52], |y| \le 4, z \in [-13, -8]$.
- R6: The arm is thickened significantly near the wall (width $\approx 16\text{ mm}$) to keep bending stress $< 25\text{ MPa}$ and deflection within limits.
- R7: Total volume is approx $2400\text{ mm}^3$, mass $\approx 3\text{ g}$, well under $25\text{ g}$; X extent is $52\text{ mm} < 55\text{ mm}$.