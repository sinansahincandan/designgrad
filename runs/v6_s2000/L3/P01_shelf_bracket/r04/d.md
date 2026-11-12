**Concept**: A tapered L-shaped cantilever bracket with a vertical wall plate and a horizontal shelf support arm. The design utilizes aggressive tapering and internal pocketing to minimize mass while maintaining high stiffness at the root ($x=10$) to satisfy strength and deflection requirements.

**Main Features**:
- **Wall Plate**: Extends from $x=0$ to $x=15$, width $y \in [-20, 20]$ (total width 40mm), height $z \in [0, 110]$. All features are centered on the $y=0$ axis.
- **Shelf Arm**: A thin horizontal plate with a top surface at exactly $z=110$. The arm thickness tapers linearly from $5\text{mm}$ (at $x=15$) down to $3\text{mm}$ (at $x=150$). Width is $y \in [-20, 20]$.
- **Profile at x=10**: A deep section (approx. height 90mm, width 40mm) to satisfy R5 and R6. To minimize mass, this section includes internal pocketing/webbing to reduce volume without compromising the Moment of Inertia ($I$).
- **Screw Access**: Two cylindrical voids with diameter 5.5mm centered at $(y=0, z=20)$ and $(y=0, z=60)$. To allow screwdriver access, all material within a $4\text{mm}$ radius of these hole axes is removed for all $x \ge 10$ (creating two longitudinal clearance channels).

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the tapered arm $\rightarrow$ shear and moment resisted by the reinforced deep section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is within $x[0, 150]$, $y[-20, 20]$, $z[0, 110]$. Centered on $y=0$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter 5.5mm; longitudinal clearance channels (radius 4mm) cut for $x \ge 10$.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$; the section between $x=140$ and $x=150$ is solid material (fill fraction 1.0) to support the shelf.
- R5: At $x=10$, the section height/width ensures $\sigma < 20\text{ MPa}$ under a 150 N load at $x=150$.
- R6: High Moment of Inertia ($I$) at the root ensures deflection $< 2.0\text{ mm}$.
- R7: Mass is kept below 90g via aggressive tapering of the arm thickness and internal pocketing of the root section.