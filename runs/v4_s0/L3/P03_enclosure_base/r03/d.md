**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor & Walls (Base Block)**: A solid structure consisting of a 2mm thick floor ($z=0$ to $z=2$) and continuous side walls with an outer perimeter of 85x55mm, reaching a height of $z=31$.
- **Bosses**: Four cylindrical pillars centered at $(\pm35, \pm20)$ with a 6mm OD, extending from the top of the floor ($z=2$) up to the bottom of the board cavity ($z=8$).
- **Board Cavity**: A large rectangular void defined by $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- **USB-C Cutout**: A through-hole rectangular aperture on the $-X$ face.
- **Pilot Holes**: Four 2.2mm diameter holes located within the bosses.

**Construction Logic (Boolean Sequence)**:
1.  **Union**: Create a base block from the floor and walls, then add the four cylindrical bosses to form a single solid mass.
2.  **Subtract Board Space**: Perform a subtractive Boolean operation using a rectangular box of $80 \times 50 \times 24\text{ mm}$ ($x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$).
3.  **Subtract USB-C Cutout**: Perform a subtractive Boolean operation using a rectangular box extending from the outer wall to the inner cavity ($x \in [-42.5, 0], y \in [-4.5, 4.5], z \in [12.5, 15.5]$).
4.  **Subtract Pilot Holes**: Perform subtractive Boolean operations for four $2.2\text{ mm}$ diameter holes centered at $(\pm35, \pm20)$, extending from $z=8$ down to $z=4$.

**Load Path**: PCB weight is transferred through screws into the pilot holes of the bosses, which distribute the load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via a strictly ordered Boolean sequence (Union $\rightarrow$ Subtractions).
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by subtraction of $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, extending from $z=2$ to $z=8$; pilot holes 2.2mm diameter from $z=8$ down to $z=4$ (4mm depth).
- R6: USB-C cutout on $-X$ wall ($x=-42.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$, acting as a through-hole to the cavity.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.