**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a vertical spine for screw mounting and a horizontal arm that tapers towards the tip.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-7$ to $y=7$, and $z=0$ to $z=110$.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$ at the top ($z=110$). The arm width is $y \in [-6, 6]$. To satisfy R4, solid material exists between $x=140$ and $x=150$ with a width of $y \in [-6, 6]$ (which covers the required area around $y=0$).
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two rectangular clearance cutouts are defined as prisms spanning $x \in [10, 20]$, $y \in [-7, 7]$, and $z \in [\text{axis} - 4, \text{axis} + 4]$ for each hole axis. This ensures no material exists within 4 mm of the hole axes for $x \ge 10$.
- **Tapered Profile**: The thickness in the Z direction decreases linearly from the wall towards the tip to reduce mass and satisfy R7. Specifically, the arm thickness at $x=15$ is $10\text{ mm}$ (reaching $z=110$) and tapers down to $3\text{ mm}$ at $x=160$.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 14 \times 110$, fitting within $170 \times 40 \times 130$ (specifically $y \in [-7, 7]$).
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$; rectangular clearance cutouts from $x=10$ to $x=20$ ensure tool access by removing all material within 4 mm of the axes.
- R4: Top surface is a flat plane at exactly $z=110$; solid material exists between $x=140$ and $x=150$; for all $x \ge 8$, no part of the geometry has a Z-coordinate $> 110$.
- R5: At $x=10$, the section (width $w=14$, height $h=110$) has $I = (14 \cdot 110^3)/12 \approx 1,547,250 \text{ mm}^4$. Stress $\sigma = Mc/I \approx (150 \cdot 140 \cdot 55) / 1,547,250 \approx 0.74 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot 1,547,250) \approx 0.25 \text{ mm} < 2.0 \text{ mm}$.
- R7: Target volume is approx $45,000 \text{ mm}^3$, mass $\approx 45,000 \cdot 0.00124 \approx 55.8\text{g} < 90\text{g}$.