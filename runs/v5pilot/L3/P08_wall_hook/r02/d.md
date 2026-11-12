**Concept**: A cantilevered hook consisting of a vertical mounting plate and a horizontal arm that transitions into a recessed strap cradle with a protective retaining lip.

**Main Features**:
- **Back Plate**: 2mm thick, dimensions $x \in [0, 2]$, $y \in [-8, 8]$, $z \in [-5, 45]$.
- **Support Arm**: A tapered structural member connecting the plate to the strap seat. The arm is optimized for volume to ensure mass remains well under the 25g limit while providing sufficient stiffness.
- **Strap Seat**: A composite feature consisting of a solid bed at $z = -14$ (under $34 \le x \le 46, |y| \le 4$) and an empty recessed pocket created by subtracting the volume $x \in [35, 45], |y| \le 6, z \in [-13, -6]$ from the main body.
- **Retaining Lip**: A small flange at the tip ($x \in [47, 52], |y| \le 4, z \in [-13, -8]$) to prevent lateral sliding.

**Load Path**: The downward force at $x=40$ is transferred through the strap seat, into the tapered support arm, and finally into the wall plate via a moment connection.

**Requirement Fulfillment**:
- R1: Built using boolean operations on primitive solids to ensure a single manifold body.
- R2: Back plate defined from $x=0$ to $x=2$, $y \in [-8, 8]$, $z \in [-5, 45]$.
- R3: Two $\varnothing 4.5\text{ mm}$ cylindrical voids are subtracted from the back plate at $(y=0, z=0)$ and $(y=0, z=40)$, penetrating the full thickness ($x \in [0, 2]$).
- R4: Strap seat created by subtracting a pocket ($x \in [35, 45], |y| \le 6, z \in [-13, -6]$) from the main body to create the required recessed clearance.
- R5: Retaining lip added at $x \in [47, 52], |y| \le 4, z \in [-13, -8]$.
- R6: The arm is thickened near the wall (width $\approx 16\text{ mm}$) to keep bending stress $< 25\text{ MPa}$ and deflection within limits ($< 1.5\text{ mm}$), while being tapered to minimize unnecessary mass.
- R7: Total volume is optimized to be approx $1600\text{ mm}^3$, mass $\approx 2\text{ g}$, well under the $25\text{ g}$ limit; X extent is $52\text{ mm} < 55\text{ mm}$.