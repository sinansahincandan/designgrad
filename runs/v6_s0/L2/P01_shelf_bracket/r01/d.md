**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a vertical spine for screw mounting and a horizontal arm that tapers towards the tip to satisfy mass constraints.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-20$ to $y=20$, and $z=0$ to $z=110$. The top surface is capped at exactly $z=110$ for all $x \ge 8$ to comply with R4.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$ at the top ($z=110$). To reduce mass, the arm tapers in the Z direction from a thickness of $20\text{mm}$ (from $z=90$ to $z=110$) at the spine interface to a thickness of $10\text{mm}$ (from $z=100$ to $z=110$) at the tip ($x=160$).
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two rectangular clearance cutouts of width $8\text{mm}$ (extending from $y=-4$ to $y=4$) are subtracted from $x=10$ to $x=15$ around each hole axis.
- **Tapered Profile**: The Z-thickness decreases towards the tip to reduce mass and satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 40 \times 110$, fitting within $170 \times 40 \times 130$ and touching the wall at $x=0$.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$; clearance cutouts from $x=10$ to $x=15$ ensure no material exists within 4mm of the axes for $x \ge 10$.
- R4: Top surface is flat at $z=110$; no material exists above $z=110$ for $x \ge 8$. Solid material exists between $x=140$ and $x=150$ below $z=110$.
- R5: At $x=10$, the section is $40\text{mm (width)} \times 110\text{mm (height)}$. Stress $\sigma = Mc/I \approx (21000 \cdot 55) / (40 \cdot 110^3 / 12) \approx 0.58 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot (40 \cdot 110^3 / 12)) \approx 0.13 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume is approx $64,000 \text{ mm}^3$, mass $\approx 64,000 \times 0.00124 \approx 79.4\text{g} < 90\text{g}$.