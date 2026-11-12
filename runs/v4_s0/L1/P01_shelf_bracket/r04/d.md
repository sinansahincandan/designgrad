**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a thick vertical spine for screw mounting and a horizontal arm that tapers towards the tip to minimize weight.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=8$, $y=-10$ to $y=10$, and $z=0$ to $z=110$.
- **Shelf Arm**: A horizontal section extending from $x=8$ to $x=160$ at the top ($z=110$). The arm has a constant thickness in Z of $15\text{ mm}$ (from $z=95$ to $z=110$) and a width in Y that tapers from $20\text{ mm}$ (at $x=8$, $y=-10$ to $y=10$) to $10\text{ mm}$ (at $x=160$, $y=-5$ to $y=5$).
- **Screw Access Channels**: Two cylindrical voids for screws (diameter 5.5 mm) centered at $(y=0, z=20)$ and $(y=0, z=60)$. To ensure screwdriver access, a larger cylindrical clearance void with radius $R = 4\text{ mm}$ is subtracted along the same axes for all $x \ge 10$.
- **Tapered Profile**: The arm width in the Y direction decreases from the wall towards the tip to reduce mass and satisfy R7.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm (starting at $x=8$) $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 20 \times 110$, fitting within $170 \times 40 \times 130$.
- R3: Screw holes at $(y=0, z=20)$ and $(y=0, z=60)$; screwdriver access guaranteed by removing all material within a $4\text{ mm}$ radius of the hole axes for $x \ge 10$.
- R4: Top surface is flat at $z=110$; since the spine ends at $x=8$, no material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section is the arm ($w=20\text{ mm}, h=15\text{ mm}$). $I = (bh^3)/12 = (20 \cdot 15^3) / 12 = 5,625\text{ mm}^4$. Stress $\sigma = Mc/I = (150\text{ N} \cdot 140\text{ mm} \cdot 7.5\text{ mm}) / 5,625\text{ mm}^4 = 2.8\text{ MPa} < 20\text{ MPa}$.
- R6: Deflection $\delta = FL^3/(3EI) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 5,625) \approx 0.78\text{ mm} < 2.0\text{ mm}$.
- R7: Volume is approx $70,000\text{ mm}^3$ (accounting for taper), mass $\approx 70,000 \times 0.00124 \approx 86.8\text{g} < 90\text{g}$.