**Concept**: A tapered, hollowed L-shaped cantilever bracket designed for high stiffness-to-weight ratio. The design utilizes a thin-walled vertical wall plate and a hollowed shelf arm to minimize mass while maintaining structural integrity at the root via an optimized hollow rectangular section and ensuring a solid contact zone at the tip.

**Main Features**:
- **Wall Plate**: A thin vertical plate extending from $x=0$ to $x=15$, constrained strictly to width $y \in [-20, 20]$.
- **Shelf Arm**: A horizontal support reaching $z=110$, extending to $x=150$. The arm is a hollowed structure that maintains a continuous, solid top surface at $z=110$. Specifically, for the region $x \in [140, 150]$ and $y \in [-20, 20]$, the material must be a solid slab (fill fraction = 1.0) to provide a stable shelf rest, before transitioning into the hollowed profile for the remainder of the arm.
- **Profile at x=10**: A hollow rectangular section (approx. height 90mm, width 40mm) to satisfy R5 (strength) and R6 (stiffness) while drastically reducing volume compared to a solid section. The screw and clearance cylinders must be subtracted from this profile to ensure the voids are continuous through both the wall plate and the arm.
- **Screw Access & Clearance**: To satisfy R3, perform two distinct sets of boolean subtractions: 
    1. Subtract two cylindrical voids (diameter 5.5mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending from $x=0$ to $x=150$.
    2. Subtract two larger cylindrical "clearance channels" (diameter $\ge 8\text{mm}$ to ensure a 4mm radius of empty space) centered on the same axes, extending from $x=10$ through to $x=150$ to provide unobstructed screwdriver access.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the hollowed arm $\rightarrow$ shear and moment resisted by the high-inertia hollow section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is strictly within $x[0, 170]$, $y[-20, 20]$, and $z[0, 130]$. Total width is exactly 40mm centered on $y=0$.
- R3: Screw holes at $(y=0, z=20)$ and $(y=0, z=60)$ with diameter 5.5mm; additionally, subtract two cylindrical voids with radius $\ge 4\text{mm}$ centered on these axes for all $x \in [10, 150]$ to create unobstructed screwdriver access channels.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$. Crucially, for the segment $x \in [140, 150]$, the section must be a solid block (no internal voids) to ensure a fill fraction of 1.0 in the support zone. No material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the hollow section provides sufficient Moment of Inertia ($I$) such that $\sigma = M \cdot c / I \le 20\text{ MPa}$ (where $M = 150\text{ N} \times 140\text{ mm}$).
- R6: The high $I$ of the hollowed root section ensures tip deflection $\delta = FL^3/(3EI) \le 2.0\text{ mm}$.
- R7: Mass is kept $< 90\text{g}$ by using thin walls and a hollow profile at the root, targeting a total volume $\le 72,500\text{ mm}^3$ (given PLA density $1.24\text{ g/cm}^3$).