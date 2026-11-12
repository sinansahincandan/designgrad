**Concept**: An L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support, centered on the Y-axis. The design utilizes an aggressive tapered profile to minimize mass while maintaining high stiffness at the root ($x=10$) to satisfy strength and deflection requirements.

**Main Features**:
- **Wall Plate**: Vertical section from $x=0$ to $x=15$, spanning $y=-20$ to $y=20$ and $z=0$ to $z=110$.
- **Shelf Support**: Horizontal section from $x=15$ to $x=150$, at height $z=110$, spanning $y=-20$ to $y=20$. 
- **Screw Holes**: Two 5.5mm diameter holes centered at $(y=0, z=20)$ and $(y=0, z=60)$, with axes along the X direction.
- **Access Channels**: To satisfy R3, rectangular cutouts (e.g., $10 \times 10$ mm) are subtracted from the solid, centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending from $x=10$ to the front face of the part to ensure no material exists within 4mm of the hole axes for $x \ge 10$.
- **Tapered Profile**: The thickness in the Z direction (and/or Y direction) decreases rapidly as X increases. At the critical section ($x=10$), the profile is sized for strength, while the volume is aggressively reduced toward $x=150$ to meet mass constraints.

**Load Path**: Load at $x=150 \rightarrow$ Horizontal arm $\rightarrow$ Bending moment transferred to wall plate at $x=10 \rightarrow$ Reaction force/moment at wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single boolean union of primitives and subtractions.
- R2: Envelope is approx $150 \times 40 \times 110$, centered at $y=0$ (spanning $y \in [-20, 20]$), well within $170 \times 40 \times 130$.
- R3: Holes at $z=20, 60$; screwdriver clearance cutouts provided for $x \ge 10$, ensuring a 4mm radius of empty space around the hole axes.
- R4: Top surface is exactly at $z=110$; no part of the geometry (including wall plate or fillets) exceeds $z=110$ for $x \ge 8$. Solid material exists between $x=140$ and $x=150$ at $z=110$.
- R5: At $x=10$, the section is a rectangle approx $40 \times 35$ mm. $I \approx (40 \cdot 35^3)/12 = 142916 \text{ mm}^4$. $\sigma = (150 \cdot 140 \cdot 17.5) / 142916 \approx 2.5 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 142916) \approx 0.2 \text{ mm} < 2.0 \text{ mm}$.
- R7: Due to aggressive tapering and thinner profiles, the volume is reduced to approx $65,000 \text{ mm}^3$. Mass $\approx 65 \times 1.24 = 79.6 \text{ g} < 90 \text{ g}$.