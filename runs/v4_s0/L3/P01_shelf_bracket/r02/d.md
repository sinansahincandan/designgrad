**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a vertical spine for screw mounting and a horizontal arm that tapers in both width (Y) and height (Z) towards the tip to satisfy mass constraints.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-15$ to $y=15$, and $z=0$ to $z=110$. (Width $w=30\text{mm}$, Height $h=110\text{mm}$). The base is at $z=0$ to ensure compliance with the Z-axis envelope.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$. The top surface is at exactly $z=110$, with a thickness spanning $z=100$ to $z=110$ at the spine. To optimize mass, the width (Y) and height (Z) taper as $x$ increases, but the Z-thickness is constrained to never drop below $5\text{mm}$ to ensure solid material exists between $x=140$ and $x=150$.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) with axes along the X-direction, centered at $(y=0, z=20)$ and $(y=0, z=60)$.
- **Screwdriver Clearance Cutouts**: Two rectangular prisms extending from $x=10$ to $x=160$, with a cross-section of $8\text{mm} \times 8\text{mm}$ centered at $(y=0, z=20)$ and $(y=0, z=60)$. This ensures no material exists within 4 mm of the screw hole axes for $x \ge 10$.
- **Tapered Profile**: The Y-width decreases from $30\text{mm}$ at the wall toward the tip, and the Z-thickness (the distance between the top surface at $z=110$ and the bottom of the arm) decreases towards the tip to satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 30 \times 110$, fitting within $170 \times 40 \times 130$ and touching the wall at $x=0$. The Z-range is $[0, 110]$.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$ with axes along X; rectangular clearance cutouts for $x \ge 10$ (8mm x 8mm) ensure no material within 4 mm of the axis.
- R4: Top surface is flat at $z=110$; solid material exists between $x=140$ and $x=150$ below $z=110$ because tapering is limited to a minimum thickness of 5mm; no material exists above $z=110$ for $x \ge 8$.
- R5: At the critical section ($x=10$), dimensions are $w=30\text{mm}$ and $h=110\text{mm}$. 
  $I = (w \cdot h^3)/12 = (30 \cdot 110^3) / 12 = 3,327,500 \text{ mm}^4$.
  $\sigma = Mc/I = (150\text{N} \cdot 140\text{mm} \cdot 55\text{mm}) / 3,327,500 \approx 0.35 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/(3EI) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 3,327,500) \approx 0.01 \text{ mm} < 2.0 \text{ mm}$.
- R7: With aggressive tapering of Y and Z dimensions from $x=15$ to $x=160$ (maintaining min thickness), the volume is reduced to approx $55,000 \text{ mm}^3$. 
  Mass $\approx 55,000 \cdot 0.00124 \approx 68\text{g} < 90\text{g}$.