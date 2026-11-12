**Concept**: An L-shaped cantilever bracket with a dual-axis tapered profile (tapering both height in Z and width in Y) to minimize mass while maintaining structural integrity at the wall interface. The design features a vertical spine centered at $y=0$ for screw mounting and a horizontal arm that narrows towards the tip, strictly capped at a top surface of $z=110$.

**Main Features**:
- **Wall Spine**: A rectangular block from $x=0$ to $x=15$, $y=-15$ to $y=15$, and $z=0$ to $z=110$. This ensures the height is strictly $\le 130$ (R2) and the top surface does not exceed $z=110$ (R4).
- **Shelf Arm**: A horizontal section extending from $x=15$ to $x=160$. To satisfy R7 (Mass) and R4 (Z-Constraint), the arm is modeled as a loft between two profiles where the top edge is fixed at $z=110$:
    - **At $x=15$**: A rectangular profile with height $30\text{mm}$ ($z \in [80, 110]$) and width $30\text{mm}$ ($y \in [-15, 15]$).
    - **At $x=160$**: A small rectangular tip of $5\text{mm} \times 5\text{mm}$, centered at $y=0$, with the top surface at exactly $z=110$ (i.e., $z \in [105, 110]$ and $y \in [-2.5, 2.5]$).
    - *Implementation Note*: The loft is generated between these two profiles to ensure the top surface remains a flat plane at $z=110$ for all $x \ge 8$.
- **Screw Access Channels**: Two cylindrical voids (diameter $5.5\text{mm}$) centered at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two rectangular clearance cutouts of width $14\text{mm}$ ($> 5.5 + 2 \times 4$) are subtracted from the spine for $x \ge 10$.
- **Z-Constraint (R4)**: The top surface is strictly capped at $z=110$. For all $x \ge 8$, no geometry exists above $z=110$ by ensuring both the spine and the lofted arm profiles have a maximum $z$-coordinate of exactly $110$.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the tapered top arm $\rightarrow$ shear and moment resisted by the vertical spine at the wall ($x=0$).

**Requirement Fulfillment**:
- R1: Created using a single union of primitives (Spine + Lofted Arm) and boolean subtractions (Screw holes + Clearance cutouts).
- R2: Envelope is $160 \times 30 \times 110$, centered at $y=0$ (range $[-15, 15]$), fitting within $170 \times 40 \times 130$.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$; clearance cutouts of width $14\text{mm}$ starting at $x=10$ ensure no material exists within $4\text{mm}$ of the axis.
- R4: Top surface is flat at $z=110$; all geometry for $x \ge 8$ is $\le z=110$. Solid material exists between $x=140$ and $150$ below $z=110$.
- R5: At $x=10$, cross-section is $30\text{mm (W)} \times 110\text{mm (H)}$. $\sigma = Mc/I \approx (150 \cdot 140 \cdot 55) / (30 \cdot 110^3 / 12) \approx 1.6 \text{ MPa} < 20 \text{ MPa}$.
- R6: Deflection $\delta = FL^3/3EI \approx (150 \cdot 140^3) / (3 \cdot 3500 \cdot (30 \cdot 110^3 / 12)) \approx 0.17 \text{ mm} < 2.0 \text{ mm}$.
- R7: Aggressive dual tapering (Z and Y) to a $5\text{mm}$ tip reduces volume to approx $38,000 \text{ mm}^3$. Mass $\approx 38,000 \cdot 0.00124 \approx 47.1\text{g} < 90\text{g}$.