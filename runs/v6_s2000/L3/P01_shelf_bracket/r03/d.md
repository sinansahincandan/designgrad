**Concept**: A tapered L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support arm. The profile utilizes a hollowed/I-beam geometry to maximize the second moment of area ($I$) at the root while aggressively minimizing mass through tapering.

**Main Features**:
- **Wall Plate**: Extends from $x=0$ to $x=15$, centered on the Y-axis with width $y \in [-20, 20]$.
- **Shelf Arm**: A horizontal support at $z=110$, extending to $x=150$. To satisfy R4, the section between $x=140$ and $x=150$ is a solid plate with no internal voids.
- **Profile Strategy**: At $x=10$, the profile uses a hollowed or I-beam shape (approx. height 90mm, width 40mm) to maximize stiffness ($I$) while minimizing cross-sectional area. The cross-sectional area decreases linearly/parabolically from $x=10$ to $x=150$.
- **Screw Access**: Two cylindrical screw holes at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two larger cylindrical clearance channels (diameter $\ge 8\text{mm}$) are subtracted from the arm starting at $x=10$ to allow screwdriver access.

**Construction Method**:
- **R1 Compliance**: All features (wall plate, arm, screw holes, and clearance channels) must be generated using a single base primitive followed by boolean subtractions to ensure a single valid solid.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the hollowed/tapered arm $\rightarrow$ shear and moment resisted by the high-$I$ section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid via boolean operations on a base primitive.
- R2: Envelope is within $x[0, 170]$, $y[-20, 20]$, $z[0, 130]$ and touches the wall at $x=0$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; clearance channels (diameter $\ge 8\text{mm}$) cut for $x \ge 10$ to ensure no material is within 4mm of the hole axes.
- R4: Top surface is a solid, continuous plate at $z=110$ from $x=140$ to $x=150$ (fill fraction 1.0); no part of the bracket exceeds $z=110$ for $x \ge 8$.
- R5: At $x=10$, the hollowed/I-beam section provides sufficient $I$ such that $\sigma = M \cdot c / I \le 20\text{ MPa}$ (where $M = 150\text{ N} \times 140\text{ mm}$).
- R6: High Moment of Inertia ($I$) at the root ensures deflection $\delta = F \cdot L^3 / (3 \cdot E \cdot I) \le 2.0\text{ mm}$.
- R7: Volume is kept low via aggressive tapering and a hollowed arm profile to ensure total volume $< 72\text{ cm}^3$ (Mass $< 90\text{g}$ using PLA density $1.24\text{ g/cm}^3$).