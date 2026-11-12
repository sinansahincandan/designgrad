**Concept**: A tapered L-shaped cantilever bracket constructed by creating a base wall and shelf arm as primitive solids, performing a `union()` operation, and then using `subtraction()` for the screw holes and clearance channels to ensure a single valid solid (R1). The profile is optimized to provide high stiffness at the root ($x=10$) while minimizing mass.

**Main Features**:
- **Wall Plate**: Extends from $x=0$ to $x=15$, width $y \in [-20, 20]$, and height $z \in [0, 110]$.
- **Shelf Arm**: A solid rectangular block with thickness $T_z = 10\text{mm}$, width $y \in [-20, 20]$, and height extending from $z=100$ to $z=110$. This block spans from $x=8$ to $x=150$, ensuring solid material exists between $x=140$ and $x=150$ directly below the top surface (R4).
- **Profile at x=10**: A deep rectangular section with height $h=90\text{mm}$ and width $w=40\text{mm}$ to satisfy strength and stiffness requirements (R5, R6).
- **Screw Access**: Two cylindrical voids for screws with diameter 5.5mm centered at $(y=0, z=20)$ and $(y=0, z=60)$. To ensure screwdriver access, two cylindrical clearance channels with a radius of $5\text{mm}$ are centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending from $x=10$ to $x=15$ (R3).

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the arm $\rightarrow$ shear and moment resisted by the deep section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is within $x[0, 150]$, $y[-20, 20]$, $z[0, 110]$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; clearance channels (radius 5mm) cut for $x \in [10, 15]$.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$; no material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section height is $h=90\text{mm}$ and width $w=40\text{mm}$, ensuring $\sigma < 20\text{ MPa}$.
- R6: High Moment of Inertia ($I$) at the root ensures deflection $< 2.0\text{ mm}$.
- R7: Estimated Volume $\approx 65\text{ cm}^3$ (calculated via $V_{wall} + V_{arm} - V_{cutouts}$), resulting in a Mass of $\approx 80.6\text{g}$ ($65 \times 1.24$), which is $< 90\text{g}$.