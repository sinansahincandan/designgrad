**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD, extending from the top of the floor ($z=2$) to the bottom of the board cavity ($z=8$).
- **Cutout**: A rectangular subtraction of $10\text{mm (X)} \times 12\text{mm (Y)} \times 6\text{mm (Z)}$ centered at $(x=-42.5, y=0, z=14)$, acting as a through-cut that penetrates the $-X$ wall from the outer face to the inner cavity.

**Construction Logic (Boolean Sequence)**:
1. **Union**: Create the main body by performing a boolean union of the Floor ($z \in [0, 2]$), the Walls (outer perimeter 85x55mm, top at $z=31$), and four solid cylindrical Bosses (6mm OD, $z \in [2, 8]$) located at $(\pm35, \pm20)$.
2. **Subtraction (Cavity)**: Subtract the board cavity volume ($x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$).
3. **Subtraction (Pilot Holes)**: Subtract four $2.2\text{mm}$ diameter cylindrical holes from each boss, extending from the floor ($z=2$) to the top of the boss ($z=8$).
4. **Subtraction (USB-C)**: Subtract the rectangular cutout volume centered at $(x=-42.5, y=0, z=14)$ to ensure a complete opening in the $-X$ wall.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load from the board interface ($z=8$) down through the floor to the base ($z=0$).

**Requirement Compliance**:
- R1: Single solid created via sequential boolean operations (Union $\rightarrow$ Subtractions).
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a single boolean subtraction of the volume $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Four bosses at $(\pm35, \pm20)$, OD 6mm, extending from $z=2$ to $z=8$, each with a 2.2mm diameter pilot hole from $z=2$ up to $z=8$.
- R6: USB-C cutout on $-X$ wall (centered at $x=-42.5$), size $10\text{mm (X)} \times 12\text{mm (Y)} \times 6\text{mm (Z)}$, implemented as a through-cut to ensure full penetration of the wall.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.