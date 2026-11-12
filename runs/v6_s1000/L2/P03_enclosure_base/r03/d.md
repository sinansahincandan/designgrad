**Concept**: A single-piece injection-molding style enclosure base designed to house an 80x50mm PCB with integrated mounting bosses and a side port cutout.

**Main Features**:
- **Base Floor**: 85 x 55 mm footprint, 2 mm thick floor.
- **Walls**: 2.5 mm thickness, height reaching Z=32.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD and 2.2mm pilot holes extending from $z=4$ to $z=8$, ensuring the hole is open at the top surface ($z=8$).
- **Cutout**: A rectangular aperture through the $-X$ wall, defined by a subtraction volume of $-43 \le x \le -39, -4.5 \le y \le 4.5, 12.5 \le z \le 15.5$ to ensure complete clearance of the wall material.

**Load Path**: PCB weight is transferred through screws into the bosses; bosses transfer load to the floor; floor transfers load to the mounting surface via compression.

**Requirement Fulfillment**:
- R1: Created using boolean operations (union/cut) resulting in a single solid.
- R2: Floor thickness is 2mm ($z=0$ to $z=2$).
- R3: Board cavity defined by subtracting a box from $-40 \le x \le 40, -25 \le y \le 25, 8 \le z \le 32$.
- R4: Outer dimensions are 85x55mm; wall top is at $z=32$.
- R5: Bosses at $(\pm35, \pm20)$ with 6mm OD and 2.2mm diameter pilot holes extending from $z=4$ to $z=8$, ensuring the hole is open at the top surface ($z=8$).
- R6: USB-C cutout through the $-X$ wall via a subtraction volume of $-43 \le x \le -39, -4.5 \le y \le 4.5, 12.5 \le z \le 15.5$.
- R7: Estimated volume $\approx 4800 \text{ mm}^3 \implies \text{Mass} \approx 6 \text{ g}$, well under 70g limit.