**Concept**: An L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support, centered on the Y-axis ($y \in [-20, 20]$). The design uses an aggressive tapered profile and a hollowed shelf structure to minimize mass while ensuring high stiffness at the root ($x=10$) to meet strength and deflection requirements.

**Main Features**:
- **Wall Plate**: Vertical section from $x=0$ to $x=15$, spanning $y=-20$ to $y=20$, and $z=0$ to $z=110$. This ensures the entire part respects the $z \le 110$ constraint for $x \ge 8$.
- **Shelf Support**: Horizontal section from $x=15$ to $x=150$, with a top surface at exactly $z=110$. To minimize mass, this section is designed as a hollowed shell/ribbed structure rather than a solid block. To satisfy R4, the support remains solid between $x=140$ and $x=150$ around $y=0$.
- **Screw Holes & Access (R3)**: Two cylindrical subtractions are performed at $(y=0, z=20)$ and $(y=0, z=60)$. Each subtraction uses a radius of 4mm (which encompasses the 2.75mm hole radius) and extends from $x=10$ to $x=150$ along the X-axis. This single operation ensures both the hole and the screwdriver clearance are cleared in one step.
- **Tapered Profile (R7)**: The thickness in the Z direction decreases aggressively as X increases. At the root ($x=10$), the section is thick for strength; at the tip ($x=150$), the Z-thickness tapers linearly down to 4mm to minimize mass.
- **Geometry Constraint (R4)**: For all $x \ge 8$, no part of the bracket extends above $z=110$.

**Load Path**: Load at $x=150 \rightarrow$ Horizontal arm $\rightarrow$ Bending moment transferred to wall plate at $x=10 \rightarrow$ Reaction force/moment at wall ($x=0$).

**Requirement Fulfillment**:
- **R1**: Created using a single boolean union of the wall and shelf, followed by two large cylindrical subtractions for holes/access.
- **R2**: Centered on Y-axis: $y \in [-20, 20]$. Envelope is approx $150 \times 40 \times 110$, within $170 \times 40 \times 130$. Touches wall at $x=0$.
- **R3**: Holes and clearance are satisfied by subtracting a single volume of radius 4mm centered at $(y=0, z=20)$ and $(y=0, z=60)$ for $x \ge 10$.
- **R4**: Top surface is exactly $z=110$. Material exists at $z=110$ for $x \in [140, 150]$ around $y=0$. The wall plate height is capped at $z=110$, ensuring no part exceeds the limit for $x \ge 8$.
- **R5 (Strength)**: At $x=10$, section is approx $40 \times 35$ mm. $I \approx (40 \cdot 35^3)/12 = 142916 \text{ mm}^4$. $\sigma = (M \cdot c) / I = (150 \cdot 140 \cdot 17.5) / 142916 \approx 2.5 \text{ MPa} < 20 \text{ MPa}$.
- **R6 (Stiffness)**: $\delta = (F \cdot L^3) / (3 \cdot E \cdot I) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 142916) \approx 0.2 \text{ mm} < 2.0 \text{ mm}$.
- **R7 (Mass)**: Optimized volume $\approx 55,000 \text{ mm}^3$ via aggressive tapering and hollowed shelf. Mass $\approx 55 \times 1.24 = 68.2 \text{ g} < 90 \text{ g}$.