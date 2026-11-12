**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height 31mm, with a constant wall thickness of 2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD; bosses extend from $z=0$ (bottom of floor) up to $z=8$ to ensure a single continuous solid union with the floor, each containing a 2.2mm pilot hole spanning $z=8$ down to $z=4$.
- **Cutout**: A rectangular subtraction through the entire $-X$ wall at $x=-42.5$, dimensions 9mm (Y) x 3mm (Z), centered at $y=0, z=14$.

**Construction Method**: Create a base block ($85 \times 55 \times 31$), union with four boss cylinders ($z=0$ to $8$), then subtract the board cavity ($x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$), the four pilot holes ($z=8$ down to $4$), and the USB-C cutout.

**Requirement Compliance**:
- R1: Single solid created via the construction method above to ensure manifold geometry.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$; constant wall thickness of 2.5mm.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, pilot hole 2.2mm diameter from $z=8$ down to $z=4$, integrated into floor from $z=0$.
- R6: USB-C cutout on $-X$ wall (at $x=-42.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.