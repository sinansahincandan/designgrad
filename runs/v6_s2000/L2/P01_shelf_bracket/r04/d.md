**Concept**: A tapered, hollowed L-shaped cantilever bracket designed for high stiffness-to-weight ratio. The design utilizes a thin-walled vertical wall plate and a hollowed shelf arm to minimize mass while maintaining structural integrity at the root via an optimized hollow rectangular section and ensuring a solid contact zone at the tip.

**Main Features**:
- **Wall Plate**: A thin vertical plate extending from $x=0$ to $x=15$, constrained strictly to width $y \in [-20, 20]$.
- **Shelf Arm**: A horizontal support reaching $z=110$, extending to $x=150$. The arm is a hollowed structure that maintains a continuous, solid top surface at $z=110$. Specifically, for the region $x \in [140, 150]$ and $y \in [-20, 20]$, the material must be a solid slab (fill fraction = 1.0) to provide a stable shelf rest, before transitioning into the hollowed profile for the remainder of the arm.
- **Profile at x=10**: A hollow rectangular section (approx. height 90mm, width 40mm) to satisfy R5 (strength) and R6 (stiffness) while drastically reducing volume compared to a solid section.
- **Screw Access & Clearance**: This feature is implemented via two distinct sets of boolean subtractions to ensure both fastener fit and tool access:
    - **Set A (Screw Holes)**: Two cylinders with diameter 5.5mm centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending from $x=0$ through the entire thickness of the wall plate to ensure the screw threads have a path.
    - **Set B (Clearance Channels)**: Two larger cylinders with radius 4.0mm (diameter 8.0mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending from $x=10$ through to the front face of the part ($x=150$). This ensures a continuous void for screwdriver access as required by R3.
    - **Note**: The subtraction of both Set A and Set B must be the final operation performed on the main body to ensure no material exists within the specified radii.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the hollowed arm $\rightarrow$ shear and moment resisted by the high-inertia hollow section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is strictly within $x[0, 170]$, $y[-20, 20]$, and $z[0, 130]$. Total width is exactly 40mm centered on $y=0$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; clearance channels (radius 4mm) cut via boolean subtraction for all $x \ge 10$ to ensure screwdriver access. This is achieved by performing two separate boolean subtractions: first, subtract two 5.5mm diameter cylinders for the screw axes; second, subtract two 8.0mm diameter cylinders (radius 4mm) starting from x=10 to ensure a continuous void for screwdriver access.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$. Crucially, for the segment $x \in [140, 150]$, the section must be a solid block (no internal voids) to ensure a fill fraction of 1.0 in the support zone. No material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the hollow section provides sufficient Moment of Inertia ($I$) such that $\sigma = M \cdot c / I \le 20\text{ MPa}$ (where $M = 150\text{ N} \times 140\text{ mm}$).
- R6: The high $I$ of the hollowed root section ensures tip deflection $\delta = FL^3/(3EI) \le 2.0\text{ mm}$.
- R7: Mass is kept $< 90\text{g}$ by using thin walls and a hollow profile at the root, targeting a total volume $\le 72,500\text{ mm}^3$ (given PLA density $1.24\text{ g/cm}^3$).