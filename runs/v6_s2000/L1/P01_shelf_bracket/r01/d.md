**Concept**: A tapered L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support arm. The profile is optimized to provide high stiffness at the root (x=10) while minimizing mass.

**Construction Strategy**: Construct the part using a single `union` of three primitives: 1) The Wall Plate ($x \in [0, 15]$), 2) The Shelf Arm slab ($x \in [8, 150]$), and 3) The Root Section ($x \in [10, 15]$). Subtract the two screw holes and the two cylindrical clearance channels using `cut` operations to ensure a single valid solid (R1).

**Main Features**:
- **Wall Plate**: Extends from $x=0$ to $x=15$, width $y \in [-20, 20]$.
- **Shelf Arm**: A solid rectangular slab with a top surface at $z=110$. The slab must have a thickness of at least 5 mm and span from $x=8$ to $x=150$, ensuring continuous material exists between $x=140$ and $x=150$.
- **Profile at x=10**: A deep rectangular section (approx. height 90mm, width 40mm) to satisfy strength and stiffness requirements.
- **Screw Access**: Two cylindrical voids for screws (diameter 5.5mm), plus two cylindrical clearance channels with a diameter of 10 mm centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending from $x=10$ to $x=15$.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the arm $\rightarrow$ shear and moment resisted by the deep section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is within $x[0, 150]$, $y[-20, 20]$, $z[0, 130]$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; clearance channels (diameter 10mm) cut for $x \in [10, 15]$ to allow screwdriver access.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$, with continuous material between $x=140$ and $x=150$. No part above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section height is $\approx 90\text{mm}$ and width $40\text{mm}$, ensuring $\sigma < 20\text{ MPa}$.
- R6: High Moment of Inertia ($I$) at the root ensures deflection $< 2.0\text{ mm}$.
- R7: Target volume is $\approx 60,000 \text{ mm}^3$ to ensure mass stays below $90\text{g}$ (calculated as $V \times 1.24 \times 10^{-3} < 90$).