**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD, extending from the top of the floor ($z=2$) up to the underside of the board ($z=8$).
- **Cutout**: Rectangular aperture on the $-X$ face for cable access.

**Load Path**: PCB weight is transferred through screws into the bosses; the bosses provide a solid interface between the floor and the board cavity, ensuring load is distributed into the base structure.

**Requirement Compliance**:
- R1: Single solid created via a specific boolean sequence: First, perform a union of the floor ($z \in [0,2]$), walls (up to $z=31$), and bosses ($z \in [2,8]$); then, subtract the board cavity (R3) and the USB-C cutout (R6).
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, extending from $z=2$ to $z=8$. Each boss contains a 2.2mm diameter pilot hole subtracted from the top ($z=8$) down to $z=4$, ensuring a 4mm deep hole within the solid boss material.
- R6: USB-C cutout on $-X$ wall (at $x=-42.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.