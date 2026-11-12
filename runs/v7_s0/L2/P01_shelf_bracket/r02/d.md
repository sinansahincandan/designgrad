**Concept**: An L-shaped cantilever bracket designed for wall mounting. The design features a vertical spine centered on $y=0$ for screw mounting and a horizontal shelf arm that provides a solid platform for the load. To optimize mass while maintaining strength, the spine width is reduced, and the profile is managed to stay within weight limits.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-10$ to $y=10$, and $z=0$ to $z=110$. (Centered on $y=0$ to satisfy R2).
- **Shelf Arm**: A solid rectangular prism extending from $x=15$ to $x=160$ at the top, with a constant thickness from $z=100$ to $z=110$. This ensures a fully solid section between $x=140$ and $x=150$ to satisfy R4.
- **Screw Access Channels**: 
    - **Holes**: Two cylindrical voids (radius $r = 2.75\text{ mm}$) with axes extending from $x=0$ to $x=15$ at $(y=0, z=20)$ and $(y=0, z=60)$.
    - **Clearance Cutouts**: To satisfy R3 (no material within 4mm of axis for $x \ge 10$), two rectangular prisms are subtracted. Each cutout has a width $\Delta y = 8\text{ mm}$ (covering $y \in [-4, 4]$) and a height $\Delta z = 8\text{ mm}$ (covering $z \in [axis-4, axis+4]$), spanning from $x=10$ to $x=15$.
- **Profile Optimization**: The spine is kept at a width of $20\text{mm}$ to reduce mass while providing sufficient moment of inertia for R5 and R6.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the solid horizontal arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives (Spine + Arm) and boolean subtractions (Holes + Clearance cutouts).
- R2: Envelope is approx $160 \times 20 \times 110$, fitting within $170 \times 40 \times 130$ and centered at $y=0$.
- R3: Holes are located at $(x, y, z)$ axes from $x=0$ to $x=15$ at $(0, 20)$ and $(0, 60)$. Clearance cutouts are rectangular prisms of $8\text{mm (width)} \times 8\text{mm (height)}$ spanning $x=10$ to $x=15$. This ensures that for all points where $x \ge 10$, the distance from any point in the solid to the hole axes is $> 4\text{ mm}$ because the material is removed within a $\pm 4\text{mm}$ bounding box of the axis.
- R4: Top surface is flat at $z=110$; the arm is a solid block from $z=100$ to $z=110$, ensuring solid support between $x=140$ and $x=150$. No material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section is roughly $20\text{mm (width)} \times 110\text{mm (height)}$. Stress $\sigma = Mc/I \approx (21000 \cdot 55) / (20 \cdot 110^3 / 12) \approx 1.65 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot (20 \cdot 110^3 / 12)) \approx 0.25 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume $\approx [ (15 \times 20 \times 110) + (145 \times 20 \times 10) ] = 33,000 + 29,000 = 62,000 \text{ mm}^3$. Mass $\approx 62,000 \cdot 0.00124 \approx 76.8\text{g} < 90\text{g}$.