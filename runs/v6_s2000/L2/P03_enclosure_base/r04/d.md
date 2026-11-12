**Concept**: A compact injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB, featuring integrated screw bosses contained within the floor thickness and a side cutout for connectivity.

**Main Features**:
- **Outer Dimensions**: 85 x 55 mm footprint with a height of 32 mm.
- **Internal Cavity**: 80 x 50 mm clear space from $z=8$ to $z=32$.
- **Screw Bosses**: Four $\varnothing 7$ mm cylinders located at $(\pm 35, \pm 20)$, extending from $z=0$ to $z=8$, each with a $\varnothing 2.2$ mm hole (depth 6 mm) starting from the top ($z=8$) and extending downwards.
- **USB Cutout**: A $9 \times 3$ mm rectangular aperture on the $-X$ wall.

**Load Path**: PCB weight is transferred through screws into the boss tops at $z=8$; bosses transfer load through the 8 mm thick floor to the mounting surface.

**Requirement Fulfillment**:
- R1: Created using a single boolean union of the base, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor thickness is 8 mm (from $z=0$ to $z=8$), exceeding the 2 mm minimum.
- R3: A central void is subtracted from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions are 85 x 55 mm; wall top is at $z=32$.
- R5: Four bosses at $(\pm 35, \pm 20)$ with $\varnothing 7$ mm OD, spanning $z \in [0, 8]$, each with a $\varnothing 2.2$ mm hole extending from $z=8$ down to $z=2$ (depth 6 mm).
- R6: USB-C cutout centered at $(-42.5, 0, 14)$ measuring $9 \times 3$ mm.
- R7: Estimated volume is $\approx 48\text{ cm}^3$, mass $\approx 60\text{ g}$ (under the 70g limit).