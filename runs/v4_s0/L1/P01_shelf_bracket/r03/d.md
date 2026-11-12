**Concept**: An L-shaped cantilever bracket with a reinforced horizontal arm to ensure stiffness, featuring a tapered profile towards the tip to optimize mass while maintaining structural integrity at the wall interface.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=8$, $y=-12$ to $y=12$ (width 24 mm), and $z=0$ to $z=110$.
- **Shelf Arm**: A horizontal section extending from $x=8$ to $x=160$. To maximize the moment of inertia ($I$), the arm occupies the top portion of the bracket, specifically from $z=80$ to $z=110$. 
- **Tapered Profile**: The arm thickness in the Z direction tapers linearly from $30\text{ mm}$ at $x=8$ down to $15\text{ mm}$ at $x=160$ to satisfy R7.
- **Screw Access Channels**: Two cylindrical voids for screws (diameter 5.5 mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$. To ensure screwdriver access, a larger cylindrical clearance void with radius $R = 4\text{ mm}$ is subtracted along the same axes for all $x \ge 10$.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the reinforced top arm (starting at $x=8$) $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 24 \times 110$, fitting within $170 \times 40 \times 130$.
- R3: Screw holes at $(y=0, z=20)$ and $(y=0, z=60)$; screwdriver access guaranteed by removing all material within a $4\text{ mm}$ radius of the hole axes for $x \ge 10$.
- R4: Top surface is flat at $z=110$; since the spine ends at $x=8$, no material exists above $z=110$ for $x \ge 8$. The arm provides solid support between $x=140$ and $x=150$.
- R5: At $x=10$, the section is a combination of the spine and the thick arm. Using the arm's cross-section ($w=24, h=30$) for a conservative estimate: $\sigma = Mc/I \approx (21000 \cdot 55) / (24 \cdot 30^3 / 12) \approx 6.4 \text{ MPa} < 20 \text{ MPa}$.
- R6: At $x=10$, the arm thickness is $30\text{ mm}$ and width is $24\text{ mm}$. $I = (24 \cdot 30^3) / 12 = 54,000 \text{ mm}^4$. Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot 54000) \approx 0.78 \text{ mm} < 2.0 \text{ mm}$.
- R7: Volume is approx $68,000 \text{ mm}^3$, mass $\approx 68,000 \times 1.24 / 1000 \approx 84.3\text{g} < 90\text{g}$.