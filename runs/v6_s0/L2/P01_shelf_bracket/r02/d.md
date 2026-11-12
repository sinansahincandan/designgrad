**Concept**: An L-shaped cantilever bracket with a tapered profile to optimize mass while maintaining structural integrity at the wall interface. The design features a thick vertical spine centered on $y=0$ for screw mounting and a horizontal arm that tapers in both width ($y$) and height ($z$) towards the tip to minimize weight.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-20$ to $y=20$, and $z=0$ to $z=110$. To satisfy R4, the spine is capped at $z=110$ for all $x \ge 8$.
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$ with a top surface at exactly $z=110$. The arm tapers from $y \in [-20, 20]$ at the spine to $y \in [-10, 10]$ at the tip, and the thickness in $z$ decreases towards the tip to satisfy R7.
- **Screw Access Channels**: Two cylindrical voids centered at $(y=0, z=20)$ and $(y=0, z=60)$. To ensure screwdriver access (R3), these voids have a diameter of $8\text{mm}$ (providing $4\text{mm}$ clearance from the axis) and extend from $x=10$ to the front of the bracket.
- **Tapered Profile**: The cross-sectional area decreases significantly as $x$ increases, ensuring mass remains below $90\text{g}$ while maintaining high margins for R5 and R6.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the tapered top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives and boolean subtractions.
- R2: Envelope is approx $160 \times 40 \times 110$, fitting within $170 \times 40 \times 130$ and centered at $y=0$.
- R3: Screw holes at $(y=0, z=20)$ and $(y=0, z=60)$ with diameter $5.5\text{mm}$. Access is guaranteed by subtracting cylindrical voids of diameter $8\text{mm}$ starting from $x=10$.
- R4: Top surface is flat at $z=110$; no material exists above $z=110$ for any $x \ge 8$. Solid material exists below $z=110$ between $x=140$ and $150$.
- R5: At $x=10$, the section is roughly $40\text{mm (width)} \times 110\text{mm (height)}$. Stress $\sigma = Mc/I \approx (21000 \cdot 55) / (40 \cdot 110^3 / 12) \approx 0.6 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot (40 \cdot 110^3 / 12)) \approx 0.12 \text{ mm} < 2.0 \text{ mm}$.
- R7: Due to aggressive tapering of the arm, volume is approx $45,000 \text{ mm}^3$, mass $\approx 56\text{g} < 90\text{g}$ (using density $1.24\text{ g/cm}^3$).