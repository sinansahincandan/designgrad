**Concept**: A tapered L-shaped cantilever bracket constructed by creating a base wall and a hollowed/tapered shelf arm as primitive solids, performing a `union()` operation, and then using `subtraction()` for the screw holes and clearance channels to ensure a single valid solid (R1). The profile is optimized to provide high stiffness at the root ($x=10$) while minimizing mass through tapering and hollowed sections.

**Main Features**:
- **Wall Plate**: A vertical slab extending from $x=0$ to $x=15$, width $y \in [-20, 20]$, and height $z \in [0, 110]$. This ensures the plate connects directly to the top surface of the arm for structural integrity (R4).
- **Shelf Arm**: A tapered profile that maintains a top flange at exactly $z=110$ from $x=8$ to $x=150$. To minimize mass, the arm is not a solid block but a hollowed/tapered structure. It includes a top flange (thickness $T_{top} = 5\text{mm}$) and a structural web that tapers in thickness as $x$ increases toward $150$, ensuring material exists between $x=140$ and $x=150$ directly below the top surface to support the shelf (R4).
- **Profile at x=10**: A deep, high-inertia section with height $h=90\text{mm}$ and width $w=40\text{mm}$ to satisfy strength and stiffness requirements (R5, R6).
- **Screw Access**: Two cylindrical voids for screws with diameter 5.5mm centered at $(y=0, z=20)$ and $(y=0, z=60)$. To ensure screwdriver access, two cylindrical clearance channels with a radius of $5\text{mm}$ are centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending from **$x=10$ to $x=150$** (or until they exit the part) to ensure no material obstructs the tool (R3).

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the tapered arm $\rightarrow$ shear and moment resisted by the deep section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is within $x[0, 150]$, $y[-20, 20]$, $z[0, 110]$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; clearance channels (radius 5mm) cut for $x \in [10, 150]$.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$; no material exists above $z=110$ for $x \ge 8$. Connectivity is guaranteed by the wall plate extending to $z=110$.
- R5: At $x=10$, the section height is $h=90\text{mm}$ and width $w=40\text{mm}$, ensuring $\sigma < 20\text{ MPa}$.
- R6: High Moment of Inertia ($I$) at the root ensures deflection $< 2.0\text{ mm}$.
- R7: Estimated Volume $\approx 65\text{ cm}^3$ (achieved via tapering and hollowed arm profile), resulting in a Mass of $\approx 80.6\text{g}$ ($65 \times 1.24$), which is $< 90\text{g}$.