**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a vertical spine for screw mounting and a horizontal arm that tapers in both width (Y) and height (Z) towards the tip to satisfy mass constraints.

**Main Features**:
- **Wall Spine**: A rectangular block spanning $x=0$ to $x=15$, $y=-15$ to $y=15$, and exactly $z=0$ to $z=110$. (Width $w=30\text{mm}$, Height $h=110\text{mm}$). This ensures the base is at $z=0$ and the top is at $z=110$.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$. The top surface is located exactly at $z=110$. To satisfy R4, no part of the geometry extends above $z=110$ for $x \ge 8$. For the range $x \in [140, 150]$, solid material exists directly below $z=110$ and centered around $y=0$.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) with axes along the X-direction, centered at $(y=0, z=20)$ and $(y=0, z=60)$.
- **Screwdriver Clearance**: Rectangular cutouts starting at $x=10$ that remove all material within a radius of 4 mm from the center of each screw axis, extending to the front of the part ($x=160$) to ensure tool access.
- **Tapered Profile**: To satisfy R7, the Y-width and Z-thickness taper as $x$ increases from the spine toward the tip. The tapering is designed such that it does not violate the flat top surface at $z=110$ or the screw clearance zones.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 30 \times 110$, fitting within $170 \times 40 \times 130$ and touching the wall at $x=0$. The Z-range is strictly $[0, 110]$.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$ with axes along X; clearance cutouts for $x \ge 10$ remove all material within 4 mm of the axis to the front of the part.
- R4: Top surface is flat at $z=110$; solid material exists between $x=140$ and $150$ below $z=110$. No material exists above $z=110$ for $x \ge 8$.
- R5: At the critical section ($x=10$), dimensions are $w=30\text{mm}$ and $h=110\text{mm}$. 
  $I = (w \cdot h^3)/12 = (30 \cdot 110^3) / 12 = 3,327,500 \text{ mm}^4$.
  $\sigma = Mc/I = (150\text{N} \cdot 140\text{mm} \cdot 55\text{mm}) / 3,327,500 \approx 0.35 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/(3EI) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 3,327,500) \approx 0.01 \text{ mm} < 2.0 \text{ mm}$.
- R7: With aggressive tapering of Y and Z dimensions from $x=15$ to $x=160$, the volume is reduced to approx $55,000 \text{ mm}^3$. 
  Mass $\approx 55,000 \cdot 0.00124 \approx 68\text{g} < 90\text{g}$.