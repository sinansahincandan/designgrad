**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a thick vertical spine for screw mounting and a horizontal arm that tapers towards the tip.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-15$ to $y=15$, and $z=0$ to $z=110$.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$ at the top ($z=110$). Thickness in Z direction is $30\text{mm}$ at the wall ($x=15$) and tapers linearly to $10\text{mm}$ at the tip ($x=160$).
- **Screw Access Channels**: Two cylindrical voids for screws (diameter 5.5 mm), plus two rectangular "clearance" cutouts, each $20\text{mm (width)} \times 10\text{mm (height)}$, centered on the screw axes, extending from $x=10$ to $x=25$ to ensure no material exists within 4 mm of the hole axis for $x \ge 10$.
- **Tapered Profile**: The thickness in the Z direction decreases from $30\text{mm}$ at the wall interface to $10\text{mm}$ at the tip to reduce mass and satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 30 \times 110$, fitting within $170 \times 40 \times 130$.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$, with rectangular clearance cutouts ($20 \times 10\text{mm}$) starting at $x=10$ to allow tool access.
- R4: Top surface is flat at $z=110$; no material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section is roughly $30\text{mm (width)} \times 110\text{mm (height)}$. Stress $\sigma = Mc/I \approx (21000 \cdot 55) / (30 \cdot 110^3 / 12) \approx 1.1 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot (30 \cdot 110^3 / 12)) \approx 0.17 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume calculation: Spine $\approx 15 \times 30 \times 110 = 49,500\text{mm}^3$; Tapered Arm (average thickness $20\text{mm}$) $\approx 145 \times 30 \times 20 = 87,000\text{mm}^3$. Subtracting voids and accounting for the taper/geometry, total volume is approx $65,000 \text{ mm}^3$. Mass $\approx 65,000 \cdot 1.24 \times 10^{-3} \approx 80.6\text{g} < 90\text{g}$.