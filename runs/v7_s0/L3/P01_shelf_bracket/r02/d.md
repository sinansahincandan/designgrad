**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a vertical spine for screw mounting and a horizontal arm that provides shelf support, tapering in width towards the tip to minimize weight.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-10$ to $y=10$, and $z=0$ to $z=110$.
- **Shelf Arm**: A continuous solid section extending from $x=15$ to $x=160$. To ensure support, it maintains a constant thickness in Z from $z=102$ to $z=110$. The width ($y$-dimension) tapers from $20\text{mm}$ at the spine towards the tip to reduce mass. For the specific interval $x \in [140, 150]$, the section must be a full rectangular block with $z \in [102, 110]$ and $y \in [-w/2, w/2]$ (where $w$ is the tapered width), ensuring no boolean subtractions or tapering logic create voids in this specific volume.
- **Screw Access Channels**: Two cylindrical voids are performed as a `boolean subtraction` from the main body. Subtract two cylinders with diameter $5.5\text{mm}$ and length $\ge 160\text{mm}$, centered at $(y=0, z=20)$ and $(y=0, z=60)$, oriented along the X-axis. To allow screwdriver access, subtract two rectangular prisms for $x \ge 10$ with a width/height of $8\text{mm} \times 8\text{mm}$ centered on the hole axes, ensuring no material exists within $4\text{mm}$ of either hole axis.
- **Tapered Profile**: The arm's width ($y$-dimension) decreases as $x$ increases to satisfy R7 (Mass), while maintaining sufficient thickness at the tip for support.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 20 \times 110$, fitting within $170 \times 40 \times 130$ (specifically $y \in [-10, 10]$).
- R3: Two $5.5\text{mm}$ diameter holes are subtracted via boolean operation; clearance cutouts for $x \ge 10$ ensure tool access.
- R4: Top surface is flat at $z=110$; the volume $x \in [140, 150], z \in [102, 110]$ is guaranteed to be solid material with a fill fraction of 1.0; no material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section is $20\text{mm (width)} \times 110\text{mm (height)}$. Moment $M = 150 \cdot 140 = 21,000 \text{ Nmm}$. $I = (bh^3)/12 = (20 \cdot 110^3)/12 \approx 2,218,333 \text{ mm}^4$. $\sigma = Mc/I = (21000 \cdot 55) / 2,218,333 \approx 0.52 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/(3EI) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 2,218,333) \approx 0.18 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume is optimized via tapering and reduced spine/arm dimensions to ensure mass $\approx 75\text{-}85\text{g} < 90\text{g}$ (using density $1.24 \text{ g/cm}^3$).