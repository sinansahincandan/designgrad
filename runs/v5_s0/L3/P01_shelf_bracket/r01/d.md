**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a thick vertical spine for screw mounting and a horizontal arm that tapers in width towards the tip to reduce weight.

**Main Features**:
- **Wall Spine**: A rectangular block centered at $y=0$, extending from $x=0$ to $x=15$, $y=-15$ to $y=15$, and $z=0$ to $z=110$.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=150$ at the top ($z=110$). To reduce mass, the width ($y$-dimension) tapers from $30\text{mm}$ (at $x=15$) to $20\text{mm}$ (from $x=40$ to $x=150$).
- **Screw Access Channels**: Two cylindrical voids for screws centered at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two rectangular clearance cutouts are centered at $y=0$, extending from $x=10$ to $x=16$, ensuring no material exists within 4mm of the hole axes for $x \ge 10$.
- **Tapered Profile**: The width in the Y direction decreases towards the tip to satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $150 \times 30 \times 110$, fitting within $170 \times 40 \times 130$ and touching the wall at $x=0$.
- R3: Screw holes at $(y=0, z=20)$ and $(y=0, z=60)$; clearance cutouts from $x=10$ to $x=16$ ensure tool access.
- R4: Top surface is flat at $z=110$; solid material exists directly below $z=110$ for the interval $x \in [140, 150]$. No material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, cross-section is $b=30\text{mm}, h=110\text{mm}$. $I = (30 \cdot 110^3)/12 = 3,327,500 \text{ mm}^4$. $\sigma = Mc/I = (150 \cdot 140 \cdot 55) / 3,327,500 \approx 0.35 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/(3EI) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 3,327,500) \approx 0.038 \text{ mm} < 2.0 \text{ mm}$.
- R7: Target volume $\approx 65,000 \text{ mm}^3$. Mass $\approx 65,000 \cdot 1.24 \times 10^{-3} = 80.6\text{g} < 90\text{g}$.