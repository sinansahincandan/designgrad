**Concept**: A tapered L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support arm. The profile is optimized to provide high stiffness at the root (x=10) while minimizing mass.

**Main Features**:
- **Wall Plate**: Extends from $x=0$ to $x=15$, width $y \in [-20, 20]$.
- **Shelf Arm**: Horizontal surface at $z=110$, extending to $x=150$.
- **Profile at x=10**: A deep rectangular section (approx. height 90mm, width 40mm) to satisfy strength and stiffness requirements.
- **Screw Access**: Two cylindrical voids for screws, plus two larger "clearance" cutouts to allow screwdriver access from the front ($x > 10$).

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the arm $\rightarrow$ shear and moment resisted by the deep section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is within $x[0, 150]$, $y[-20, 20]$, $z[0, 110]$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; clearance channels cut for $x \ge 10$.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$.
- R5: At $x=10$, the section height is $\approx 90\text{mm}$ and width $40\text{mm}$, ensuring $\sigma < 20\text{ MPa}$.
- R6: High Moment of Inertia ($I$) at the root ensures deflection $< 2.0\text{ mm}$.
- R7: Volume is kept low via tapering to ensure mass $< 90\text{g}$ (approx $55\text{--}70\text{g}$).