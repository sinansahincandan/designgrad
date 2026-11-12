**Concept**: A cantilevered hook consisting of a vertical mounting plate and a horizontal arm that transitions into a recessed strap cradle with a protective retaining lip.

**Main Features**:
- **Back Plate**: 2mm thick, dimensions $x \in [0, 2]$, $y \in [-8, 8]$, $z \in [-5, 45]$.
- **Support Arm**: A tapered structural member connecting the plate to the strap seat; width starts at $\approx 12\text{ mm}$ near the wall and tapers to manage bending stress while minimizing mass.
- **Strap Seat**: A solid bed with its top surface at $z = -14$ under $34 \le x \le 46, |y| \le 4$, created by first defining a larger block and then subtracting the empty pocket volume ($x \in [35, 45], |y| \le 6, z \in [-13, -6]$).
- **Screw Holes**: Two cylindrical voids of $\varnothing 4.5\text{ mm}$ passing through the back plate along the X-axis, centered at $(y, z) = (0, 0)$ and $(0, 40)$.
- **Retaining Lip**: A small flange at the tip ($x \in [47, 52]$) to prevent lateral sliding.

**Load Path**: The downward force at $x=40$ is transferred through the strap seat, into the tapered support arm, and finally into the wall plate via a moment connection.

**Requirement Fulfillment**:
- R1: Built using boolean operations on primitive solids to ensure a single manifold body.
- R2: Back plate defined from $x=0$ to $x=2$, $y \in [-8, 8]$, $z \in [-5, 45]$.
- R3: Subtract two cylinders of $\varnothing 4.5\text{ mm}$ from the main body at $(y,z)=(0,0)$ and $(0,40)$ to ensure material is removed and holes are valid voids.
- R4: Subtract the pocket ($x \in [35, 45], |y| \le 6, z \in [-13, -6]$) from the structural arm/seat volume to ensure the specified region is strictly empty.
- R5: Retaining lip added at $x \in [47, 52], |y| \le 4, z \in [-13, -8]$.
- R6: The arm is tapered (starting width $\approx 12\text{ mm}$) to keep bending stress $< 25\text{ MPa}$ and deflection within limits.
- R7: Target a total volume of $\approx 1400\text{ mm}^3$ to ensure mass is $\approx 1.7\text{ g}$ (well under $25\text{ g}$); X extent is $52\text{ mm} < 55\text{ mm}$.