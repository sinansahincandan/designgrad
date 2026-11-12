**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined by a fillet to ensure structural integrity. The design uses a subtractive approach from two primary blocks (the face plate and the base plate) to ensure a single solid manifold.

**Main Features**:
- **Face Plate**: A solid block defined by $x \in [-35, 35]$, $z \in [0, 55]$, and $y \in [0, 4]$. This provides the structural mounting surface for the motor.
- **Base Plate**: Located at $z \in [0, 5]$ and $y \in [0, \text{thickness}]$, ensuring the part sits on the table at $z=0$.
- **Central Bore**: A $\varnothing 22.5$ mm hole centered at $(x=0, z=30)$ passing through the face plate ($y=0$ to $4$).
- **Motor Screw Holes**: Four $\varnothing 3.4$ mm holes drilled through the face plate along the Y-axis at $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- **Motor Interface**: A recessed pocket cut into the back of the face plate to accommodate the NEMA 17 body while maintaining screw alignment and clearance.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape (face plate + base plate), followed by subtractions for holes and pockets.
- R2: Face plate is a solid block with thickness 4mm ($y=0$ to $y=4$) spanning $x \in [-35, 35]$ and $z \in [0, 55]$, ensuring material remains around all bores.
- R3: Central bore $\varnothing 22.5$ mm centered at $(0, 30)$ through the face plate ($y=0$ to $4$).
- R4: Four motor holes $\varnothing 3.4$ mm at $(\pm 15.5, 30 \pm 15.5)$ subtracted from the solid face plate along the Y-axis.
- R5: A pocket is cut into the back of the face plate (at $y=0$) to ensure clearance for the motor body within the specified volume.
- R6: Two base holes $\varnothing 5.5$ mm at $(\pm 25, 25)$ in the $z=0$ plane (on the base plate).
- R7: Envelope is approx. $70 \times 55 \times 55$ mm (within $x \in [-35, 35]$ and top $\le 55$); volume is calculated to be well under the 60g limit for PLA.