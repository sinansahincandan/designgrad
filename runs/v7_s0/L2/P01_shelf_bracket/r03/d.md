**Concept**: An L-shaped cantilever bracket designed for wall mounting. The design features a vertical spine centered on $y=0$ for screw mounting and a horizontal shelf arm that provides a solid platform for the load. To optimize mass while maintaining strength, the spine width is managed to stay within weight limits while ensuring a seamless union with the arm at $x=15$.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-10$ to $y=10$, and $z=0$ to $z=110$. (Centered on $y=0$ to satisfy R2).
- **Shelf Arm**: A single, continuous solid rectangular prism extending from $x=15$ to $x=160$, with $y=-10$ to $y=10$, and a constant thickness from $z=100$ to $z=110$. This ensures the junction at $x=15$ is seamless (R1) and that the section between $x=140$ and $x=150$ is 100% solid material (R4).
- **Screw Access Channels**: Two cylindrical voids (diameter 5.5 mm) are subtracted from the spine, with axes along X at $(y=0, z=20)$ and $(y=0, z=60)$. To ensure screwdriver access (R3), two rectangular clearance cutouts ($10\text{mm}$ width $\times$ $20\text{mm}$ height) are subtracted. These cutouts are centered on the hole axes and extend from $x=10$ to $x=15$, ensuring no material exists within 4 mm of the hole axes for all $x \ge 10$.
- **Profile Optimization**: The spine and arm both maintain a width ($y$-dimension) of $20\text{mm}$ to reduce mass while providing sufficient moment of inertia for R5 and R6.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the solid horizontal arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives (Spine + Arm) followed by boolean subtractions (Holes + Clearance cutouts).
- R2: Envelope is $160 \times 20 \times 110$, fitting within $170 \times 40 \times 130$ and centered at $y=0$. Touches the wall at $x=0$.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$; rectangular cutouts (width 10mm, height 20mm) starting at $x=10$ ensure a void of at least 5mm radius around the axes for $x \ge 10$, satisfying the 4mm clearance requirement.
- R4: Top surface is flat at $z=110$; the arm is a solid block from $z=100$ to $z=110$ and $y=-10$ to $y=10$, ensuring 100% solid support between $x=140$ and $x=150$. No material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section is roughly $20\text{mm (width)} \times 110\text{mm (height)}$. Stress $\sigma = Mc/I \approx (21000 \cdot 55) / (20 \cdot 110^3 / 12) \approx 1.65 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot (20 \cdot 110^3 / 12)) \approx 0.25 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume $\approx [ (15 \times 20 \times 110) + (145 \times 20 \times 10) ] = 33,000 + 29,000 = 62,000 \text{ mm}^3$. Mass $\approx 62,000 \cdot 0.00124 \approx 76.8\text{g} < 90\text{g}$.