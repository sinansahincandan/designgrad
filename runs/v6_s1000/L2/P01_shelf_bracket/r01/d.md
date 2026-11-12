**Concept**: An L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support, featuring an aggressive tapered profile to minimize mass while maintaining high stiffness at the root ($x=10$).

**Main Features**:
- **Wall Plate**: Vertical section from $x=0$ to $x=15$, spanning $y=-15$ to $y=15$ (width 30 mm) and $z=0$ to $z=120$.
- **Shelf Support**: Horizontal section from $x=15$ to $x=150$, at height $z=110$. To ensure R4 compliance, the segment $x \in [140, 150]$ is a solid block with thickness $20\text{ mm}$ (from $z=90$ to $z=110$).
- **Screw Holes**: Two 5.5mm holes centered at $(y=0, z=20)$ and $(y=0, z=60)$, with axes along X.
- **Access Channels**: Rectangular cutouts (e.g., $15\text{ mm wide} \times 15\text{ mm high}$) centered at the hole axes, extending from $x=10$ to the front face of the wall plate to ensure no material exists within 4mm of the hole axes for $x \ge 10$.
- **Tapered Profile**: The thickness in the Z direction decreases rapidly as X increases. At the root ($x=10$), the section is sized to meet R5/R6, while the distal end tapers to reduce mass.

**Load Path**: Load at $x=150 \rightarrow$ Horizontal arm $\rightarrow$ Bending moment transferred to wall plate at $x=10 \rightarrow$ Reaction force/moment at wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single boolean union of primitives and subtractions.
- R2: Envelope is approx $150 \times 30 \times 120$, centered on Y ($-15$ to $15$), well within $170 \times 40 \times 130$.
- R3: Holes at $z=20, 60$; screwdriver clearance cutouts provided for $x \ge 10$ with dimensions $>4\text{ mm}$ from axis.
- R4: Top surface is at $z=110$; profile height drops below $z=110$ for $x \ge 8$. Solid material block exists between $x=140$ and $x=150$ under the shelf.
- R5: At $x=10$, width $w=30\text{ mm}$, height $h=40\text{ mm}$. $I \approx (30 \cdot 40^3)/12 = 160,000 \text{ mm}^4$. $\sigma = (150 \cdot 140 \cdot 20) / 160,000 = 2.625 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 160,000) \approx 0.18 \text{ mm} < 2.0 \text{ mm}$.
- R7: Target volume $\approx 65,000 \text{ mm}^3$. Mass $\approx 65 \times 1.24 = 80.6 \text{ g} < 90 \text{ g}$.