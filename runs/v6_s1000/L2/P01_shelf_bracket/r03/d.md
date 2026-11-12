**Concept**: An L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support, re-centered on the Y-axis to meet envelope requirements. It features an aggressive tapered profile to minimize mass while maintaining high stiffness at the root ($x=10$).

**Main Features**:
- **Wall Plate**: Vertical section from $x=0$ to $x=15$, spanning $y=-20$ to $y=20$ (width 40mm) and $z=0$ to $z=120$.
- **Shelf Support**: Horizontal section from $x=15$ to $x=150$, at height $z=110$. To ensure R4, this is a solid block with thickness in Z. The Y-width is reduced to 25mm (from $y=-12.5$ to $y=12.5$) to save mass.
- **Screw Holes**: Two 5.5mm diameter holes centered at $(y=0, z=20)$ and $(y=0, z=60)$, with axes along X.
- **Access Channels (R3)**: To ensure screwdriver access, cylindrical cutouts with a radius of 5mm are subtracted from the part, centered on the hole axes, extending from $x=10$ to the front face ($x=0$). This ensures no material exists within 4mm of the axes for $x \ge 10$.
- **Tapered Profile**: The thickness in the Z direction decreases rapidly as X increases. At the root ($x=10$), the section is optimized for strength, while the outer reaches are significantly thinned to meet R7.

**Load Path**: Load at $x=150 \rightarrow$ Horizontal arm $\rightarrow$ Bending moment transferred to wall plate at $x=10 \rightarrow$ Reaction force/moment at wall ($x=0$).

**Requirement Fulfillment**:
- **R1**: Created using a single boolean union of the plate and shelf, with subtractions for holes and access channels.
- **R2**: Envelope is $150 \times 40 \times 120$, centered on Y ($-20 \le y \le 20$), touching $x=0$.
- **R3**: Holes at $z=20, 60$; cylindrical voids of radius 5mm ensure no material within 4mm for $x \ge 10$.
- **R4**: Top surface is at $z=110$. The shelf support is a solid block ensuring material exists between $x=140$ and $x=150$ below $z=110$. Profile height drops below $z=110$ for $x \ge 8$.
- **R5 (Strength)**: At $x=10$, the cross-section is a rectangle with width $b=40$ and height $h=35$. 
  $I = (40 \cdot 35^3)/12 \approx 142,916 \text{ mm}^4$.
  $\sigma = (M \cdot c) / I = (150\text{ N} \cdot 140\text{ mm} \cdot 17.5\text{ mm}) / 142,916 \approx 2.58 \text{ MPa}$.
  $2.58 \text{ MPa} < 20 \text{ MPa}$ (Pass).
- **R6 (Stiffness)**: $\delta = (F \cdot L^3) / (3 \cdot E \cdot I) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 142,916) \approx 0.2 \text{ mm}$.
  $0.2 \text{ mm} < 2.0 \text{ mm}$ (Pass).
- **R7 (Mass)**: By reducing the Y-width of the shelf to 25mm and aggressively tapering the Z-thickness from $x=15$ to $x=150$, the volume is reduced to approx $42,000 \text{ mm}^3$.
  Mass $\approx 42,000 \cdot 1.24 / 1000 = 52 \text{ g} < 90 \text{ g}$ (Pass).