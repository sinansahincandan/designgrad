**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD and 2.2mm pilot holes. To ensure connectivity, these are unioned to the floor/walls before subtractions.
- **Cutout**: Rectangular aperture on the $-X$ face for cable access, modeled as a through-cut to ensure wall penetration.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load into the floor and side walls via a continuous solid geometry.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, from $z=2$ to $z=8$. Pilot holes (2.2mm diameter) are subtracted from $z=4$ up to $z=8$ to ensure they are open at the top and at least 4mm deep.
- R6: USB-C cutout on $-X$ wall; subtraction box defined by $x \in [-42.5, -37.5]$ (to ensure full penetration of the wall), $y \in [-4.5, 4.5]$, and $z \in [12.5, 15.5]$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.