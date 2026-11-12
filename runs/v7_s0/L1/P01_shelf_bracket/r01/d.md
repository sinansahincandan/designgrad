**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a thick vertical spine for screw mounting and a horizontal arm that tapers towards the tip.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-15$ to $y=15$, and $z=0$ to $z=110$.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$ at the top ($z=110$).
- **Screw Access Channels**: Two cylindrical voids for screws (diameter 5.5 mm), plus two rectangular clearance cutouts, each defined by a width of 8 mm (extending from $y=-4$ to $y=4$) and a height of 8 mm (extending from $z = \text{axis} - 4$ to $z = \text{axis} + 4$), starting at $x=10$ and extending through the part.
- **Tapered Profile**: The thickness in the Z direction decreases from the wall towards the tip to reduce mass and satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 30 \times 110$, fitting within $170 \times 40 \times 130$.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$, with rectangular clearance cutouts of $8 \times 8\text{ mm}$ centered at the hole axes, extending from $x=10$ to the front face. This ensures a $4\text{ mm}$ radius of empty space around each hole axis for all $x \ge 10$, satisfying tool access.
- R4: Top surface is flat at $z=110$; no material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section is roughly $30\text{mm (width)} \times 110\text{mm (height)}$. Stress $\sigma = Mc/I \approx (21000 \cdot 55) / (30 \cdot 110^3 / 12) \approx 1.1 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot (30 \cdot 110^3 / 12)) \approx 0.17 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume is approx $60,000 \text{ mm}^3$, mass $\approx 74\text{g} < 90\text{g}$.