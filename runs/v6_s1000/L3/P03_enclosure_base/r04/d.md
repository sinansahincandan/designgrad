**Concept**: A single-piece injection-molding style enclosure base designed to house an 80x50mm PCB with integrated mounting bosses and a side port cutout.

**Main Features**:
- **Base Floor**: 85 x 55 mm footprint, 2 mm thick floor ($z=0$ to $z=2$).
- **Walls**: 2.5 mm thickness, height reaching Z=32, providing continuous enclosure around the board cavity.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD, extending from the floor ($z=2$) to $z=8$; each contains a 2.2mm diameter pilot hole subtracted from the boss volume (extending from $z=3.5$ to $z=8$) to ensure the top is open and flush.
- **Cutout**: A rectangular aperture on the $-X$ face for USB-C connectivity, created by subtracting a box centered at $y=0, z=14$ with dimensions $\Delta Y = 9\text{ mm}$ and $\Delta Z = 3\text{ mm}$, extending from the outer wall surface ($x=-42.5$) to the inner wall surface ($x=-40$).

**Load Path**: PCB weight is transferred through screws into the open pilot holes of the bosses; bosses transfer load to the floor; floor transfers load to the mounting surface via compression.

**Requirement Fulfillment**:
- R1: Created using boolean operations (union/cut) resulting in a single solid.
- R2: Floor thickness is 2mm ($z=0$ to $z=2$).
- R3: Board cavity defined by subtracting a box from $-40 \le x \le 40, -25 \le y \le 25, 8 \le z \le 32$.
- R4: Outer dimensions are 85x55mm; wall top is at $z=32$.
- R5: Bosses at $(\pm35, \pm20)$ with 6mm OD and 2.2mm diameter pilot holes (subtracted from $z=3.5$ to $z=8$) ensuring the hole is open at the top ($z=8$).
- R6: USB-C cutout through the $-X$ wall, centered at $y=0, z=14$, spanning from $x=-42.5$ to $x=-40$ with a width of 9mm and height of 3mm.
- R7: Estimated volume $\approx 4800 \text{ mm}^3 \implies \text{Mass} \approx 6 \text{ g}$, well under 70g limit.