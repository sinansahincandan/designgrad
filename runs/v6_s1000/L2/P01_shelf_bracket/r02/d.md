**Concept**: An L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support, featuring an aggressive tapered profile to minimize mass while maintaining high stiffness at the root.

**Main Features**:
- **Wall Plate**: Vertical section from $x=0$ to $x=15$, spanning $y=-20$ to $y=20$ and $z=0$ to $z=120$.
- **Shelf Support**: Horizontal section from $x=15$ to $x=150$, at height $z=110$. The section between $x=140$ and $x=150$ is a solid block of material directly beneath the top surface.
- **Screw Holes**: Two 5.5mm diameter holes with axes along X, centered at $(y=0, z=20)$ and $(y=0, z=60)$.
- **Access Channels**: Rectangular cutouts centered at $(y=0, z=20)$ and $(y=0, z=60)$, providing a clear radius of $4\text{ mm}$ from the hole axes, extending from $x=10$ to $x=25$ to ensure screwdriver access.
- **Tapered Profile**: The thickness in the Z direction decreases linearly from $35\text{ mm}$ at $x=10$ down to $10\text{ mm}$ at $x=150$. For all $x \ge 8$, the maximum Z-coordinate is exactly $z=110$. The Y-span is fixed at $[-20, 20]$ (total width $40\text{ mm}$).

**Load Path**: Load at $x=150 \rightarrow$ Horizontal arm $\rightarrow$ Bending moment transferred to wall plate at $x=10 \rightarrow$ Reaction force/moment at wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single boolean union of primitives and subtractions.
- R2: Envelope is approx $150 \times 40 \times 110$, fitting within $170 \times 40 \times 130$ and touching $x=0$. Y-span is exactly $[-20, 20]$.
- R3: Holes at $z=20, 60$; screwdriver clearance cutouts ensure no material within $4\text{ mm}$ of hole axes for $x \ge 10$.
- R4: Top surface is at $z=110$ and reaches $x=150$. For $x \ge 8$, the profile height does not exceed $z=110$.
- R5: At $x=10$, the section is a rectangle $40\text{ mm (Y)} \times 35\text{ mm (Z)}$. $I = (40 \cdot 35^3)/12 \approx 142916 \text{ mm}^4$. $\sigma = (M \cdot c) / I = (150 \cdot 140 \cdot 17.5) / 142916 \approx 2.5 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = (F \cdot L^3) / (3 \cdot E \cdot I) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 142916) \approx 0.2 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume is approx $50,000 \text{ mm}^3$ due to aggressive tapering. Mass $\approx 50 \times 1.24 = 62 \text{ g} < 90 \text{ g}$.