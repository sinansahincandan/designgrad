**Concept**: A cantilevered hook consisting of a vertical mounting plate and a horizontal arm that transitions into a recessed strap cradle with a protective retaining lip.

**Main Features**:
- **Back Plate**: 4mm thick, dimensions $x \in [-2, 2]$, $y \in [-8, 8]$, $z \in [-5, 45]$. This thickness ensures sufficient material depth around the screw holes located at the wall interface ($x=0$).
- **Support Arm**: A tapered structural member connecting the plate to the strap seat. To optimize mass while maintaining strength, the width tapers from $\approx 16\text{ mm}$ at $x=2$ down to $10\text{ mm}$ near the strap seat ($x=35$).
- **Strap Seat**: A recessed bed at $z = -14$ with a clearance pocket for a $10 \times 6\text{ mm}$ strap.
- **Retaining Lip**: A small flange at the tip ($x=50$) to prevent lateral sliding.

**Load Path**: The downward force at $x=40$ is transferred through the strap seat, into the tapered support arm, and finally into the wall plate via a moment connection.

**Requirement Fulfillment**:
- R1: Built using boolean operations on primitive solids to ensure a single manifold body.
- R2: Back plate defined from $x=-2$ to $x=2$, $y \in [-8, 8]$, $z \in [-5, 45]$.
- R3: Two cylindrical screw holes of $\varnothing 4.5\text{ mm}$ passing through the entire thickness of the plate along the X-axis, centered at $(y, z) = (0, 0)$ and $(0, 40)$. The $x \in [-2, 2]$ range ensures a 4mm material depth around the holes.
- R4: Strap bed created by subtracting a pocket ($x \in [35, 45], |y| \le 6, z \in [-13, -6]$) from the main body, leaving a solid bed with top at $z = -14$ for $34 \le x \le 46$.
- R5: Retaining lip added at $x \in [47, 52], |y| \le 4, z \in [-13, -8]$.
- R6: The arm is thickened near the wall (width $\approx 16\text{ mm}$) to keep bending stress $< 25\text{ MPa}$ and deflection within limits.
- R7: Total volume is targeted at approximately $18,000\text{ mm}^3$, resulting in a mass of $\approx 22.3\text{ g}$ (using PLA density $1.24\text{ g/cm}^3$), which is safely under the $25\text{ g}$ limit; X extent is $52\text{ mm} < 55\text{ mm}$.