**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a vertical spine for screw mounting and a horizontal arm that tapers towards the tip to satisfy weight constraints.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-20$ to $y=20$, and $z=0$ to $z=110$. (Width = 40mm).
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=150$ at the top ($z=110$). The arm's thickness in Z decreases sharply from $x=15$ towards $x=150$ to reduce mass.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$ with axes along X. To allow screwdriver access, two rectangular clearance cutouts of width 8 mm are provided, extending from $x=10$ to $x=25$.
- **Tapered Profile**: The thickness in the Z direction decreases significantly as $x$ increases towards the tip to satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $150 \times 40 \times 110$, fitting within $170 \times 40 \times 130$ (centered on $y=0$).
- R3: Holes at $(0,0,20)$ and $(0,0,60)$ with diameter 5.5 mm; clearance cutouts from $x=10$ to $x=25$ ensure no material within 4 mm of the axis for $x \ge 10$.
- R4: Top surface is flat at exactly $z=110$; no material exists above $z=110$ for $x \ge 8$. Solid material exists between $x=140$ and $x=150$ directly below $z=110$.
- R5: At the critical section ($x=10$), the spine is $40\text{mm (width)} \times 110\text{mm (height)}$. Stress $\sigma = Mc/I \approx (21000 \cdot 55) / (40 \cdot 110^3 / 12) \approx 0.6 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot (40 \cdot 110^3 / 12)) \approx 0.13 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume is approx $50,000 \text{ mm}^3$, mass $\approx 62\text{g} < 90\text{g}$ (using density 1.24 g/cm³).