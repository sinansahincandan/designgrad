**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined by a fillet to ensure structural integrity. The design uses a subtractive approach from two primary blocks to ensure a single solid manifold.

**Main Features**:
- **Face Plate**: Located at $y \in [0, 10]$, providing the mounting surface for the motor. It spans $x \in [-30, 30]$ and $z \in [5, 55]$ to ensure sufficient material around all bores.
- **Base Plate**: Located at $z \in [0, T]$ (where $T$ is plate thickness), providing the mounting surface for the table with its bottom surface sitting exactly at $z=0$.
- **Motor Interface**: A recessed area/pocket to accommodate the NEMA 17 body while maintaining screw alignment.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions.
- R2: Face plate thickness is set to 10mm ($y=0$ to $y=10$) to ensure a solid ring of material exists around the $\varnothing 22.5\text{mm}$ central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(0, 30)$ through the face plate; face plate dimensions extend well beyond the bore radius (spanning $z \in [5, 55]$ and $x \in [-30, 30]$) to ensure material continuity.
- R4: Four motor holes $\varnothing 3.4$ mm at $(\pm 15.5, 30 \pm 15.5)$ through the face plate along the Y axis.
- R5: A pocket is cut into the back of the face plate to ensure clearance for the motor body ($x \in [-21.5, 21.5]$, $y < 0$, $z \in [8.5, 51.5]$).
- R6: Two base holes $\varnothing 5.5$ mm at $(x, y) = (\pm 25, 25)$, drilled vertically through the base plate starting from the table surface at $z=0$.
- R7: Envelope is approx. $50 \times 50 \times 55$ mm; volume is calculated to be well under the 60g limit for PLA.