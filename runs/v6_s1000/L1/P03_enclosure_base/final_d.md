**Concept**: A single-piece injection-molding style enclosure base designed to house an 80x50mm PCB with integrated mounting bosses and a side port cutout.

**Main Features**:
- **Base Floor**: 85 x 55 mm footprint, 2 mm thick floor.
- **Walls**: 2.5 mm thickness, height reaching Z=32.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD and 2.2mm pilot holes.
- **Cutout**: A rectangular aperture on the $-X$ face for USB-C connectivity.

**Load Path**: PCB weight is transferred through screws into the bosses; bosses transfer load to the floor; floor transfers load to the mounting surface via compression.

**Requirement Fulfillment**:
- R1: Created using boolean operations (union/cut) resulting in a single solid.
- R2: Floor thickness is 2mm ($z=0$ to $z=2$).
- R3: Board cavity defined by subtracting a box from $-40 \le x \le 40, -25 \le y \le 25, 8 \le z \le 32$.
- R4: Outer dimensions are 85x55mm; wall top is at $z=32$.
- R5: Bosses at $(\pm35, \pm20)$ with 6mm OD and 4.5mm deep pilot holes (extending from $z=2$ to $z=8$).
- R6: USB-C cutout at $x=-42.5$, centered at $y=0, z=14$ ($9 \times 3$ mm).
- R7: Estimated volume $\approx 4800 \text{ mm}^3 \implies \text{Mass} \approx 6 \text{ g}$, well under 70g limit.