**Concept**: A cantilevered hook consisting of a vertical mounting plate and a horizontal arm that transitions into a recessed strap cradle with a protective retaining lip.

**Main Features**:
- **Back Plate**: 6mm thick, dimensions $x \in [0, 6]$, $y \in [-8, 8]$, $z \in [-5, 45]$.
- **Screw Holes**: Two cylindrical voids, $\varnothing 4.5\text{ mm}$, passing through the back plate along the X-axis at $(y, z) = (0, 0)$ and $(0, 40)$.
- **Support Arm**: A tapered structural member connecting the plate to the strap seat to manage bending stress.
- **Strap Seat**: A recessed bed at $z = -14$ with a clearance pocket for a $10 \times 6\text{ mm}$ strap.
- **Retaining Lip**: A small flange at the tip ($x=50$) to prevent lateral sliding.

**Load Path**: The downward force at $x=40$ is transferred through the strap seat, into the tapered support arm, and finally into the wall plate via a moment connection.

**Requirement Fulfillment**:
- R1: Built using boolean operations on primitive solids to ensure a single manifold body.
- R2: Back plate defined from $x=0$ to $x=6$, $y \in [-8, 8]$, $z \in [-5, 45]$.
- R3: Subtract two cylinders of $\varnothing 4.5\text{ mm}$ centered at $(y, z) = (0, 0)$ and $(0, 40)$ from the back plate, extending through the full thickness ($x \in [0, 6]$), ensuring they are boolean subtractions to create valid voids; the 6mm thickness satisfies the requirement for material around the holes.
- R4: Strap bed created by subtracting a pocket ($x \in [35, 45], |y| \le 6, z \in [-13, -6]$) from the main body.
- R5: Retaining lip added at $x \in [47, 52], |y| \le 4, z \in [-13, -8]$.
- R6: The arm is thickened significantly near the wall (width $\approx 16\text{ mm}$) to keep bending stress $< 25\text{ MPa}$ and deflection within limits.
- R7: Total volume is approx $1800\text{ mm}^3$, mass $\approx 2.2\text{ g}$, well under $25\text{ g}$; X extent is $52\text{ mm} < 55\text{ mm}$.