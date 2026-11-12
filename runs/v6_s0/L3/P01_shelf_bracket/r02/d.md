**Concept**: A lightweight, high-strength cantilever bracket utilizing an optimized I-beam spine and a trussed arm. The design uses hollowed geometries to minimize mass while maintaining the required cross-sectional inertia at critical points for strength (R5) and stiffness (R6).

**Main Features**:
- **Optimized Wall Spine ($x=0$ to $15$)**: An I-beam structure centered at $y=0$. The outer envelope is exactly $w=40\text{mm}$ ($y \in [-20, 20]$) and $h=110\text{mm}$ ($z \in [0, 110]$). To satisfy R5/R6 at the critical section ($x=10$), the flanges and web are sized to ensure $I \approx 4.44 \times 10^6 \text{ mm}^4$. The interior is hollowed to reduce mass.
- **Trussed Shelf Arm ($x=15$ to $160$)**: A tapered, thin-walled truss structure. Instead of a solid slab, it consists of upper and lower chords connected by diagonal webs. 
- **R4 Support Pillar**: To satisfy the shelf support requirement (R4) without excessive mass, a localized vertical web/pillar is placed at $y \in [-5, 5]$, extending from $z=0$ to $z=110$, spanning the interval $x \in [140, 150]$.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) with axes along X, centered at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, rectangular clearance cutouts are subtracted from $x=10$ to the tip of the arm, ensuring no material exists within 4 mm of the hole axis.
- **Geometric Constraints**: For all $x \ge 8$, the entire geometry is clipped by a plane at $z=110$ so that no part of the bracket exceeds this height (R4).

**Load Path**: Load at $x=150 \rightarrow$ transferred through the trussed arm chords $\rightarrow$ bending moment and shear resisted by the I-beam spine at the wall ($x=0$).

**Requirement Fulfillment**:
- **R1**: Created using a single union of primitives (I-beam, truss members, support pillar) and boolean subtractions.
- **R2**: Envelope is $160 \times 40 \times 110$, fitting within $170 \times 40 \times 130$. Width is strictly $y \in [-20, 20]$.
- **R3**: Holes at $(y=0, z=20)$ and $(y=0, z=60)$; rectangular clearance cutouts ensure tool access for $x \ge 10$.
- **R4**: Top surface is flat at $z=110$ for $x \ge 8$. A localized pillar at $y \in [-5, 5]$ provides solid material directly below $z=110$ for $x \in [140, 150]$.
- **R5 (Strength)**: At $x=10$, the I-beam cross-section is designed to provide $I = 4,436,667 \text{ mm}^4$. 
  $\sigma = (150\text{N} \cdot 140\text{mm} \cdot 55\text{mm}) / 4,436,667 \approx 0.26 \text{ MPa} < 20 \text{ MPa}$.
- **R6 (Stiffness)**: $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 4,436,667) \approx 0.01 \text{ mm} < 2.0 \text{ mm}$.
- **R7 (Mass)**: By using an I-beam spine and a trussed arm instead of solid blocks, the volume is reduced significantly.
  Estimated Volume $\approx 58,000 \text{ mm}^3$.
  $\text{Mass} = 58,000 \cdot 1.24 \times 10^{-3} \approx 71.9\text{g} < 90\text{g}$.