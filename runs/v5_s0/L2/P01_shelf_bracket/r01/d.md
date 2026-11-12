**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a vertical spine for screw mounting and a horizontal arm that tapers towards the tip.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-10$ to $y=10$, and $z=0$ to $z=110$.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$ at the top ($z=110$). The arm width is constrained to $y \in [-10, 10]$ to ensure solid material exists between $x=140$ and $x=150$ around $y=0$.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two rectangular clearance cutouts span the full width of the part from $x=10$ to $x=20$ at these heights, ensuring no material exists within 4 mm of the hole axes for $x \ge 10$.
- **Tapered Profile**: The thickness in the Z direction decreases from the wall towards the tip to reduce mass and satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 20 \times 110$, fitting within $170 \times 40 \times 130$ (specifically $y \in [-10, 10]$).
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$; clearance cutouts from $x=10$ to $x=20$ ensure tool access.
- R4: Top surface is flat at $z=110$; solid material exists between $x=140$ and $x=150$; no material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section (width $w=20$, height $h=110$) has $I = (20 \cdot 110^3)/12 \approx 2,218,333 \text{ mm}^4$. Stress $\sigma = Mc/I \approx (150 \cdot 140 \cdot 55) / 2,218,333 \approx 0.52 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot 2,218,333) \approx 0.18 \text{ mm} < 2.0 \text{ mm}$.
- R7: Target volume is approx $55,000 \text{ mm}^3$, mass $\approx 55,000 \cdot 0.00124 \approx 68.2\text{g} < 90\text{g}$.