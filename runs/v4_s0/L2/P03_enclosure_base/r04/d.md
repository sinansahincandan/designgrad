**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD, spanning from the top of the floor ($z=2$) to the bottom of the board cavity ($z=8$).
- **Cutout**: Rectangular aperture on the $-X$ face for cable access.

**Construction Logic (Boolean Sequence)**:
1. Create Floor ($z \in [0, 2]$).
2. Add Bosses (cylinders at $(\pm35, \pm20)$ from $z=2$ to $z=8$).
3. Add Walls (outer perimeter 85x55mm up to $z=31$).
4. Perform Boolean Union of Floor, Bosses, and Walls to create the primary solid.
5. Subtract Board Cavity ($x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$).
6. Subtract USB-C Cutout (on $-X$ wall).
7. Subtract Pilot Holes (2.2mm diameter cylinders from the center of each boss, extending from $z=8$ down to $z=2$).

**Load Path**: PCB weight is transferred through screws into the pilot holes of the bosses; the bosses distribute this load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via sequential boolean operations (Union then Subtractions).
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, spanning $z=2$ to $z=8$; pilot holes 2.2mm diameter extending from $z=8$ down to $z=2$.
- R6: USB-C cutout on $-X$ wall (at $x=-42.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.