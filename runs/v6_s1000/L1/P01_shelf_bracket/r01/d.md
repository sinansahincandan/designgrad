**Concept**: An L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support, featuring a tapered profile to optimize mass while maintaining stiffness at the root.

**Main Features**:
- **Wall Plate**: Vertical section from $x=0$ to $x=15$, spanning $z=0$ to $z=120$.
- **Shelf Support**: Horizontal section from $x=15$ to $x=150$, at height $z=110$.
- **Screw Holes**: Two 5.5mm holes at $(y=0, z=20)$ and $(y=0, z=60)$, with axes along the X direction.
- **Access Channels**: Two rectangular cutouts of width 10 mm and height 10 mm, centered on the screw hole axes $(y=0, z=20)$ and $(y=0, z=60)$, extending from $x=10$ to $x=15$. This geometry ensures no material exists within a 4 mm radius of the hole axes for $x \ge 10$.
- **Tapered Profile**: The thickness in the Z direction decreases as X increases to reduce mass while keeping the root (at $x=10$) thick enough for strength, stiffness, and to accommodate the screw holes and access channels.

**Load Path**: Load at $x=150 \rightarrow$ Horizontal arm $\rightarrow$ Bending moment transferred to wall plate at $x=10 \rightarrow$ Reaction force/moment at wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single boolean union of primitives and subtractions.
- R2: Envelope is approx $150 \times 40 \times 110$, well within $170 \times 40 \times 130$.
- R3: Holes at $z=20, 60$; access channels are $10 \times 10$ mm cutouts starting at $x=10$, ensuring a clearance $> 4\text{ mm}$ from the hole axes for all $x \ge 10$.
- R4: Top surface is at $z=110$; profile height drops below $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section is a rectangle approx $40 \times 35$ mm. $I \approx (40 \cdot 35^3)/12 = 142916 \text{ mm}^4$. $\sigma = (150 \cdot 140 \cdot 17.5) / 142916 \approx 2.5 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 142916) \approx 0.2 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume is approx $55,000 \text{ mm}^3$. Mass $\approx 55 \times 1.24 = 68 \text{ g} < 90 \text{ g}$.