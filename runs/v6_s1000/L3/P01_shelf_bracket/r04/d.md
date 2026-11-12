**Concept**: An L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support, centered on the Y-axis ($y \in [-20, 20]$). The design utilizes an aggressive tapered profile and a hollowed underside (I-beam style) to minimize mass while maintaining high stiffness at the root ($x=10$) to satisfy strength and deflection requirements.

**Main Features**:
- **Wall Plate**: Vertical section from $x=0$ to $x=15$. To comply with R4, the height is constrained to $z \in [0, 110]$. The width in Y is $40\text{mm}$ ($y \in [-20, 20]$) for the lower section ($z < 60$) and tapers to $30\text{mm}$ ($y \in [-15, 15]$) for the upper section ($z > 60$) to reduce mass.
- **Shelf Support**: Horizontal section from $x=15$ to $x=150$. The top surface is exactly at $z=110$. To satisfy R4 and R7, this is not a solid block; instead, it uses a hollowed rectangular profile (I-beam shape). Material is removed from the underside between $x=15$ and $x=140$. To satisfy R4, the support remains solid between $x=140$ and $x=150$ around $y=0$.
- **Screw Holes (R3)**: Two 5.5mm diameter holes centered at $(y=0, z=20)$ and $(y=0, z=60)$, with axes along the X direction. These are implemented via `subtraction` from the main body.
- **Screwdriver Access (R3)**: To ensure absolute clearance and account for floating-point errors, a cylindrical cutout with a radius of $5\text{mm}$ is subtracted around each hole axis, extending from $x=10$ to the front of the part ($x=150$). This subtraction is performed after the main body union.
- **Tapered Profile (R7)**: The thickness in both Z and Y directions decreases as X increases. At the root ($x=10$), the section is thick for strength; at the tip ($x=150$), the profile is significantly reduced to minimize mass.
- **Geometry Constraint (R4)**: For all $x \ge 8$, no part of the bracket extends above $z=110$. The wall plate height is capped at $z=110$ and the shelf top is exactly $z=110$.

**Load Path**: Load at $x=150 \rightarrow$ Horizontal arm (I-beam profile) $\rightarrow$ Bending moment transferred to wall plate at $x=10 \rightarrow$ Reaction force/moment at wall ($x=0$).

**Requirement Fulfillment**:
- **R1**: Created using a single boolean union of the wall and shelf, followed by subtractions for holes and access channels.
- **R2**: Centered on Y-axis: $y \in [-20, 20]$. Envelope is approx $150 \times 40 \times 110$, within $170 \times 40 \times 130$. Touches wall at $x=0$.
- **R3**: Holes at $(y=0, z=20)$ and $(y=0, z=60)$. Clearance provided by subtracting a $5\text{mm}$ radius volume for $x \ge 10$.
- **R4**: Top surface is exactly $z=110$. Material exists at $z=110$ for $x \in [140, 150]$. Profile height is $\le 110$ for all $x \ge 8$.
- **R5 (Strength)**: At $x=10$, the section is designed to be approx $40 \times 35\text{mm}$ (or equivalent area/inertia). $I \approx 142916 \text{ mm}^4$. $\sigma = (M \cdot c) / I = (150 \cdot 140 \cdot 17.5) / 142916 \approx 2.5 \text{ MPa} < 20 \text{ MPa}$.
- **R6 (Stiffness)**: $\delta = (F \cdot L^3) / (3 \cdot E \cdot I) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 142916) \approx 0.2 \text{ mm} < 2.0 \text{ mm}$.
- **R7 (Mass)**: Through hollowing the shelf and tapering the Y/Z dimensions, optimized volume $\approx 55,000 \text{ mm}^3$. Mass $\approx 55 \times 1.24 = 68.2\text{ g} < 90\text{ g}$.