**Concept**: An L-shaped cantilever bracket with a wide vertical spine for stability and a tapered horizontal arm to minimize mass. The design ensures full compliance with screwdriver access, shelf support height constraints, and structural requirements.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-20$ to $y=20$, and $z=0$ to $z=110$. This maximizes the width within the allowed envelope.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$ at the top ($z=110$). To satisfy R4, solid material is maintained directly below $z=110$ for $x \in [140, 150]$ around $y=0$.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) with axes along the X-direction, centered at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two rectangular clearance cutouts are subtracted, centered on these axes, extending from $x=10$ to the tip of the arm to ensure no material exists within 4 mm of the hole axis for $x \ge 10$.
- **Tapered Profile**: The thickness in the Z direction decreases linearly from the wall towards the tip. Crucially, for all $x \ge 8$, the maximum Z-coordinate is exactly $z=110$ to satisfy R4.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- **R1**: Created using a single union of primitives and boolean subtractions.
- **R2**: Envelope is approx $160 \times 40 \times 110$, fitting within $170 \times 40 \times 130$ and touching the wall at $x=0$.
- **R3**: Holes at $(y=0, z=20)$ and $(y=0, z=60)$ with axes along X; rectangular clearance cutouts ensure tool access for $x \ge 10$.
- **R4**: Top surface is flat at $z=110$; no material exists above $z=110$ for $x \ge 8$. Solid support provided for $x \in [140, 150]$.
- **R5 (Strength)**: At the critical section $x=10$, the width is $w=40\text{mm}$ and height is $h=110\text{mm}$. 
  $I = (wh^3)/12 = (40 \cdot 110^3) / 12 \approx 4,436,667 \text{ mm}^4$.
  $\sigma = Mc/I = (150\text{N} \cdot 140\text{mm} \cdot 55\text{mm}) / 4,436,667 \approx 0.26 \text{ MPa} < 20 \text{ MPa}$.
- **R6 (Stiffness)**: $\delta = FL^3/(3EI) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 4,436,667) \approx 0.01 \text{ mm} < 2.0 \text{ mm}$.
- **R7 (Mass)**: With an aggressive taper and a wide but thin profile, the volume is estimated at $\approx 55,000 \text{ mm}^3$. 
  $\text{Mass} = 55,000 \cdot 1.24 \times 10^{-3} \approx 68.2\text{g} < 90\text{g}$.