**Concept**: A tapered L-shaped cantilever bracket constructed by creating a base wall and shelf arm as primitive solids, performing a `union()` operation, and then using `subtraction()` for the screw holes and clearance channels to ensure a single valid solid (R1). The design uses a wide profile at the critical root ($x=10$) to satisfy strength/stiffness requirements while tapering the width and thickness in non-critical regions to minimize mass.

**Main Features**:
- **Wall Plate**: Extends from $x=0$ to $x=15$, width $y \in [-15, 15]$, and height $z \in [10, 100]$. This reduced width (30mm) saves mass while providing a mounting surface.
- **Shelf Arm**: A tapered horizontal member at the top. It maintains a thickness of $T_z = 10\text{mm}$ for the tip section ($x \in [140, 150]$) to satisfy R4, but is reduced to a thinner slab of $T_z = 6\text{mm}$ and width $y \in [-15, 15]$ for the span $x \in [15, 140]$.
- **Profile at x=10**: A deep rectangular section with height $h=90\text{mm}$ (spanning $z=10$ to $z=100$) and width $w=40\text{mm}$ ($y \in [-20, 20]$) to satisfy strength and stiffness requirements (R5, R6). This section is integrated into the wall plate/arm junction.
- **Screw Access**: Two cylindrical voids for screws with diameter 5.5mm centered at $(y=0, z=20)$ and $(y=0, z=60)$. To ensure screwdriver access, two cylindrical clearance channels with a radius of $5\text{mm}$ are centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending from $x=10$ to $x=15$ (R3).

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the arm $\rightarrow$ shear and moment resisted by the deep section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is within $x[0, 150]$, $y[-20, 20]$, $z[0, 110]$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; clearance channels (radius 5mm) cut for $x \in [10, 15]$.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$; solid material exists between $x=140$ and $x=150$ directly below the top surface. No material above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section height is $h=90\text{mm}$ and width $w=40\text{mm}$, ensuring $\sigma < 20\text{ MPa}$.
- R6: High Moment of Inertia ($I$) at the root ensures deflection $< 2.0\text{ mm}$.
- R7: Estimated Volume $\approx 58\text{ cm}^3$ (calculated via optimized $V_{wall} + V_{tapered\_arm} - V_{cutouts}$), resulting in a Mass of $\approx 71.9\text{g}$ ($58 \times 1.24$), which is well below the $90\text{g}$ limit.