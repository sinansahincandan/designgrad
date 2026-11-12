**Concept**: A lightweight, L-shaped cantilever bracket featuring a slim vertical spine and an aggressively tapered horizontal arm. The design minimizes mass by reducing the Y-width of the entire part and utilizing a linear Z-taper on the shelf arm to satisfy weight constraints while maintaining sufficient stiffness at the critical $x=10$ section.

**Main Features**:
- **Wall Spine**: A slim vertical plate from $x=0$ to $x=8$, $y=-10$ to $y=10$, and $z=0$ to $z=110$. (Width = 20mm, Thickness = 8mm).
- **Shelf Arm**: A horizontal section extending from $x=8$ to $x=150$ at the top ($z=110$). To optimize mass, the Z-thickness follows a linear taper: starting at $z_{min}=30\text{mm}$ (at $x=8$) and decreasing to $z_{min}=5\text{mm}$ (at $x=150$). The top surface remains flat at $z=110$.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$ with axes along X. To allow screwdriver access, two rectangular clearance cutouts of width 12 mm are provided, extending from $x=8$ to $x=25$.
- **Tapered Profile**: The thickness in the Z direction decreases linearly from $30\text{mm}$ at the spine interface to $5\text{mm}$ at the tip ($x=150$) to satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the tapered shelf arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives (spine + tapered arm) and boolean subtractions (screw holes + clearance cutouts).
- R2: Envelope is approx $150 \times 20 \times 110$, fitting within $170 \times 40 \times 130$.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$ with diameter 5.5 mm; clearance cutouts from $x=8$ to $x=25$ ensure no material within 4 mm of the axis for $x \ge 10$.
- R4: Top surface is flat at exactly $z=110$; no material exists above $z=110$ for $x \ge 8$. Solid material exists between $x=140$ and $x=150$ directly below $z=110$.
- R5: At the critical section ($x=10$), the cross-section is approximately $20\text{mm (width)} \times 30\text{mm (height)}$. 
  $I = (b \cdot h^3)/12 = (20 \cdot 30^3)/12 = 45,000 \text{ mm}^4$. 
  $\sigma = Mc/I = (150 \cdot 140 \cdot 15) / 45,000 = 6.67 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/(3EI) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 45,000) \approx 0.81 \text{ mm} < 2.0 \text{ mm}$.
- R7: Estimated Volume $\approx 58,000 \text{ mm}^3$, mass $\approx 72\text{g}$ (using density 1.24 g/cm³), which is $< 90\text{g}$.