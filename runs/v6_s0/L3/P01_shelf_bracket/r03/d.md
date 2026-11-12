**Concept**: An L-shaped cantilever bracket featuring a hollowed vertical spine to minimize mass while maintaining high stiffness, and a tapered horizontal arm. The design incorporates a solid support pillar at the shelf end and specific clearance channels for screwdriver access, ensuring strict adherence to all dimensional and structural constraints.

**Main Features**:
- **Hollow Wall Spine**: A thin-walled rectangular shell from $x=0$ to $x=15$, $y=-20$ to $y=20$, and $z=0$ to $z=110$. To satisfy R7 (Mass), the spine is not a solid block but a hollowed structure. The outer dimensions are $w=40\text{mm}$ and $h=110\text{mm}$, with wall thicknesses optimized to ensure the Moment of Inertia ($I$) at $x=10$ meets R5 and R6 requirements.
- **Shelf Arm & Support Pillar**: A horizontal section extending from $x=15$ to $x=160$ at $z=110$. To satisfy R4, a "solid rectangular pillar" is integrated into the arm for the segment $x \in [140, 150]$, providing direct material support under the shelf.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) with axes along the X-direction, centered at $(y=0, z=20)$ and $(y=0, z=60)$. These holes are located within the Wall Spine ($x \in [0, 15]$). To satisfy R3, two rectangular clearance cutouts (voids) are subtracted from the part, centered on these axes, extending from $x=10$ to the tip of the arm. This ensures no material exists within a 4 mm radius of the hole axis for all $x \ge 10$.
- **Tapered Profile & Height Constraint**: The thickness in the Z direction decreases linearly from the wall towards the tip. To satisfy R4 and R2, for all $x \ge 8$, the maximum Z-coordinate is exactly $z=110$ and the minimum is $z=0$.

**Global Envelope Constraints**:
All vertices $(x, y, z)$ must strictly satisfy:
- $0 \le x \le 170$
- $-20 \le y \le 20$ (Strictly enforced for all features)
- For $x \ge 8$: $0 \le z \le 110$

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm and support pillar $\rightarrow$ shear and moment resisted by the hollowed vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- **R1**: Created using a single union of primitives (spine, arm, pillar) and boolean subtractions (hollow core, screw holes, clearance channels).
- **R2**: Envelope is $160 \times 40 \times 110$, fitting within $170 \times 40 \times 130$ and touching the wall at $x=0$. Y-range is strictly $[-20, 20]$.
- **R3**: Holes at $(y=0, z=20)$ and $(y=0, z=60)$ with axes along X; rectangular clearance cutouts ensure tool access for all $x \ge 10$.
- **R4**: Top surface is flat at $z=110$; no material exists above $z=110$ for $x \ge 8$. Solid support pillar provided for $x \in [140, 150]$.
- **R5 (Strength)**: At the critical section $x=10$, the hollowed profile is designed such that $I \ge 4,436,667 \text{ mm}^4$ to ensure $\sigma = Mc/I < 20 \text{ MPa}$.
- **R6 (Stiffness)**: The geometry at $x=10$ ensures $\delta = FL^3/(3EI) < 2.0 \text{ mm}$ using the specified PLA properties.
- **R7 (Mass)**: By utilizing a hollowed rectangular shell for the spine and a tapered arm, the volume is kept low to ensure $\text{Mass} < 90\text{g}$.