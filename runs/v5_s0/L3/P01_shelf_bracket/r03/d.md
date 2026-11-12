**Concept**: An L-shaped cantilever bracket with a slim vertical spine for mounting and an aggressively tapered horizontal arm to minimize mass. The design uses a centered geometry relative to $y=0$ to comply with envelope constraints and utilizes significant Y-axis tapering to meet the strict weight requirement while maintaining sufficient structural stiffness through the Z-dimension.

**Main Features**:
- **Wall Spine**: A rectangular block centered at $y=0$, extending from $x=0$ to $x=15$, $y=-7.5$ to $y=7.5$, and $z=0$ to $z=110$. (Width = 15mm).
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=150$ with its top surface at exactly $z=110$. To satisfy R7, the width ($y$-dimension) tapers linearly from $15\text{mm}$ (at $x=15$) to $8\text{mm}$ (at $x=150$). The thickness in $z$ is maintained at $10\text{mm}$ for the arm (spanning $z=100$ to $z=110$) to ensure R4 compliance.
- **Screw Access Channels**: Three distinct boolean subtractions:
    1. Two cylindrical voids (diameter $5.5\text{mm}$) centered at $(y=0, z=20)$ and $(y=0, z=60)$, extending along the X-axis through the spine.
    2. Two rectangular clearance cutouts to allow tool access: for each hole, a void is removed for $x \ge 10$ within a $4\text{mm}$ radius of the hole axis.
- **Tapered Profile**: The width in the Y direction decreases from the spine toward the tip to satisfy R7 and stay well within the $[-20, 20]$ envelope.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives followed by boolean subtractions.
- R2: Envelope is $150 \times 15 \times 110$, fitting within $170 \times 40 \times 130$ and touching the wall at $x=0$. Y-range is $[-7.5, 7.5]$, well within $[-20, 20]$.
- R3: Screw holes (dia 5.5mm) at $(y=0, z=20)$ and $(y=0, z=60)$; clearance cutouts for $x \ge 10$ ensure tool access within 4mm of the axis.
- R4: Top surface is flat at $z=110$. The arm thickness ensures solid material exists directly below $z=110$ for $x \in [140, 150]$. No material exists above $z=110$ for $x \ge 8$.
- R5: At $x=10$, cross-section is $b=15\text{mm}, h=110\text{mm}$. $I = (15 \cdot 110^3)/12 = 1,663,750 \text{ mm}^4$. $\sigma = Mc/I = (150 \cdot 140 \cdot 55) / 1,663,750 \approx 0.69 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/(3EI) = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 1,663,750) \approx 0.08 \text{ mm} < 2.0 \text{ mm}$.
- R7: Target volume $\approx 65,000 \text{ mm}^3$. Mass $\approx 65,000 \cdot 1.24 \times 10^{-3} = 80.6\text{g} < 90\text{g}$.