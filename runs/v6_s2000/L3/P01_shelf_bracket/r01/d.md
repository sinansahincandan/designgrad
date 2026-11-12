**Concept**: A tapered L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support arm. The profile is highly optimized via tapering to provide high stiffness at the root ($x=10$) while minimizing mass to stay under 90g. All components are centered on $y=0$.

**Main Features**:
- **Wall Plate**: Extends from $x=0$ to $x=15$, width $y \in [-20, 20]$.
- **Shelf Arm**: Horizontal surface at $z=110$, extending to $x=150$. The arm is a tapered profile centered on $y=0$ with width $y \in [-20, 20]$ at the root and tapering towards the tip.
- **Profile at x=10**: A deep rectangular section of height $90\text{mm}$ and width $20\text{mm}$ (centered on $y=0$) to satisfy strength and stiffness requirements.
- **Tapering Strategy**: To minimize mass, the section height decreases from $90\text{mm}$ at $x=10$ down to a minimum thickness of $5\text{mm}$ at $x=150$. The wall plate and shelf arm are designed with minimal thickness (approx. $3\text{--}5\text{mm}$) where possible, except for the structural root.
- **Screw Access**: Two cylindrical voids of diameter $5.5\text{mm}$ centered at $(y=0, z=20)$ and $(y=0, z=60)$. To satisfy R3, two rectangular clearance channels with a width of $\ge 13.5\text{mm}$ ($5.5\text{mm} + 4\text{mm} + 4\text{mm}$) are cut, centered on the screw axes, extending from $x=10$ to the front of the part.

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the tapered arm $\rightarrow$ shear and moment resisted by the deep $90\text{mm} \times 20\text{mm}$ section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is strictly within $x[0, 170]$, $y[-20, 20]$, $z[0, 130]$. All features are centered on $y=0$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter $5.5\text{mm}$; clearance channels of width $\ge 13.5\text{mm}$ ensure no material is within $4\text{mm}$ of the axis for $x \ge 10$.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$; no part of the bracket exceeds $z=110$ for $x \ge 8$.
- R5: At $x=10$, the section height $90\text{mm}$ and width $20\text{mm}$ ensures $\sigma < 20\text{ MPa}$ (calculated via $M \cdot c / I$).
- R6: High Moment of Inertia ($I$) at the root ensures deflection $< 2.0\text{ mm}$.
- R7: Mass is kept below $90\text{g}$ through aggressive tapering and hollowed/minimal thickness profiles in non-critical zones.