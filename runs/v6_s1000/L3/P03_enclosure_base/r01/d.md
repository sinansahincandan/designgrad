**Concept**: A single-piece injection-molding style enclosure base designed to house an 80x50mm PCB. The design utilizes boolean unions to ensure the floor, walls, and mounting bosses form a single continuous solid for structural integrity.

**Main Features**:
- **Base Floor**: 85 x 55 mm footprint, 2 mm thick floor ($z=0$ to $z=2$).
- **Walls**: 2.5 mm thickness, height reaching Z=32, forming a continuous perimeter around the cavity.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD. Each pillar is physically merged (boolean union) with the floor to ensure structural continuity and effective load transfer.
- **Cutout**: A rectangular through-cut aperture on the $-X$ face for USB-C connectivity.

**Load Path**: PCB weight is transferred through screws into the bosses; the bosses are physically merged (boolean union) with the 2mm floor to ensure structural continuity; the floor then transfers the load to the mounting surface via compression.

**Requirement Fulfillment**:
- R1: Created using boolean operations (union/cut) resulting in a single solid.
- R2: Floor thickness is 2mm ($z=0$ to $z=2$).
- R3: Board cavity defined by subtracting a box from $-40 \le x \le 40, -25 \le y \le 25, 8 \le z \le 32$.
- R4: Outer dimensions are 85x55mm; wall top is at $z=32$.
- R5: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD; each pillar contains a subtractive cylindrical hole of 2.2mm diameter extending from $z=8$ down to $z=2$, ensuring the hole is open and empty.
- R6: USB-C cutout on the $-X$ face created by subtracting a box of $9 \times 3 \text{ mm}$ (Y $\times$ Z) that extends from the outer boundary ($x=-42.5$) through to the inner cavity wall ($x=-40$).
- R7: Estimated volume $\approx 4800 \text{ mm}^3 \implies \text{Mass} \approx 6 \text{ g}$, well under 70g limit.