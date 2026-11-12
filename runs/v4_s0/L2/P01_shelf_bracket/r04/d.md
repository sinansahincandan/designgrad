**Concept**: An L-shaped cantilever bracket with a tapered profile designed to minimize mass while meeting strength, stiffness, and shelf support requirements. The design utilizes a vertical spine for wall mounting and a horizontal arm that tapers linearly in the Z direction towards the tip.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-10$ to $y=10$, and $z=0$ to $z=110$. (Width = 20mm, Height = 110mm).
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=150$. The top surface is flat at exactly $z=110$. To satisfy R4 and R7, the arm's thickness in Z tapers linearly from its bottom surface: it starts at 20mm thick at $x=15$ (bottom surface at $z=90$) and tapers down to 5mm thick at $x=150$ (bottom surface at $z=105$). This ensures solid material exists between $x=140$ and $x=150$ directly below $z=110$.
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$ with axes along X. To allow screwdriver access, two rectangular clearance cutouts of width 8 mm are provided, extending from $x=10$ to $x=25$.
- **Tapered Profile**: The Z-thickness follows a linear taper from $x=15$ ($T=20\text{mm}$) to $x=150$ ($T=5\text{mm}$), optimizing mass.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the tapered arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $150 \times 20 \times 110$, fitting within $170 \times 40 \times 130$ (centered on $y=0$).
- R3: Holes at $(0,0,20)$ and $(0,0,60)$ with diameter 5.5 mm; clearance cutouts from $x=10$ to $x=25$ ensure no material within 4 mm of the axis for $x \ge 10$.
- R4: Top surface is flat at exactly $z=110$; no material exists above $z=110$ for $x \ge 8$. Solid material exists between $x=140$ and $x=150$ directly below $z=110$ with a thickness of $\approx 5.5\text{mm}$.
- R5: At the critical section ($x=10$), the spine is $20\text{mm (width)} \times 110\text{mm (height)}$. Stress $\sigma = Mc/I = (150 \cdot 140 \cdot 55) / (20 \cdot 110^3 / 12) \approx 0.556 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI = (150 \cdot 140^3) / (3 \cdot 3500 \cdot (20 \cdot 110^3 / 12)) \approx 0.0185 \text{ mm} < 2.0 \text{ mm}$.
- R7: Estimated volume $\approx 63,500 \text{ mm}^3$, mass $\approx 78.7\text{g} < 90\text{g}$ (using density 1.24 g/cm³).