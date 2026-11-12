**Concept**: A tapered, hollowed L-shaped cantilever bracket designed for high stiffness-to-weight ratio. The design utilizes a thin-walled vertical wall plate and a hollowed shelf arm to minimize mass while maintaining structural integrity at the root via an optimized hollow rectangular section.

**Main Features**:
- **Wall Plate**: A thin vertical plate extending from $x=0$ to $x=15$, constrained strictly to width $y \in [-20, 20]$.
- **Shelf Arm**: A horizontal support reaching $z=110$, extending to $x=150$. To minimize mass, the arm is designed as a thin-walled profile (e.g., $z \in [105, 110]$) or a hollowed structure rather than a solid slab.
- **Profile at x=10**: A hollow rectangular section (approx. height 90mm, width 40mm) to satisfy R5 (strength) and R6 (stiffness) while drastically reducing volume compared to a solid section.
- **Screw Access & Clearance**: Two cylindrical voids for screws (diameter 5.5mm) at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two larger clearance channels (cylindrical or rectangular voids with radius/half-width $\ge 4\text{mm}$) are subtracted from the part, centered on the screw axes, extending from $x=10$ to the front of the part.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the hollowed arm $\rightarrow$ shear and moment resisted by the high-inertia hollow section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is strictly within $x[0, 170]$, $y[-20, 20]$, and $z[0, 130]$. Total width is exactly 40mm centered on $y=0$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; clearance channels (radius $\ge 4\text{mm}$) cut for all $x \ge 10$ to ensure screwdriver access.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$. No material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the hollow section provides sufficient Moment of Inertia ($I$) such that $\sigma = M \cdot c / I \le 20\text{ MPa}$ (where $M = 150\text{ N} \times 140\text{ mm}$).
- R6: The high $I$ of the hollowed root section ensures tip deflection $\delta = FL^3/(3EI) \le 2.0\text{ mm}$.
- R7: Mass is kept $< 90\text{g}$ by using thin walls and a hollow profile at the root, targeting a total volume $\le 72,500\text{ mm}^3$ (given PLA density $1.24\text{ g/cm}^3$).