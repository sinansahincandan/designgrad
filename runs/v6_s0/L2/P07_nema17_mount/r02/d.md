**Concept**: An L-shaped bracket constructed using an additive-first approach to ensure structural integrity. The design begins by defining a solid Face Plate and a solid Base Plate, which are then joined via a boolean union to create a single manifold. Once the primary volume is established, specific features (bore, screw holes, and clearance pockets) are removed using subtractive operations.

**Main Features**:
- **Face Plate**: A solid rectangular prism defined by $x \in [-35, 35]$, $y \in [0, 4]$, and $z \in [0, 55]$. This serves as the primary mounting surface for the motor.
- **Base Plate**: A solid rectangular prism providing the mounting surface for the table at $z=0$.
- **Motor Interface**: A recessed clearance pocket cut into the back of the face plate to accommodate the NEMA 17 body.

**Load Path**: The motor's reaction force is applied to the face plate, transferred through the solid corner junction (where the plates are unioned), and distributed through the base plate into the table via two M5 mounting screws.

**Requirement Compliance**:
- R1: Created by performing a `union` of the Face Plate and Base Plate solids, followed by sequential `cut` operations to ensure a single valid solid.
- R2: Face plate thickness is guaranteed by defining it as a solid slab from $y=0$ to $y=4$.
- R3: Central bore $\varnothing 22.5$ mm is cut through the face plate, centered at $(0, y, 30)$, spanning the full $y$-thickness.
- R4: Four motor holes $\varnothing 3.4$ mm are cut along the Y-axis at $(\pm 15.5, y, 30 \pm 15.5)$.
- R5: A clearance pocket is cut from the assembly to ensure no material exists in the volume $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$.
- R6: Two base holes $\varnothing 5.5$ mm are cut through the base plate along the Z-axis at $(x, y) = (\pm 25, 25)$.
- R7: Envelope is within $-35 \le x \le 35$, $z \le 55$ mm; mass is verified to be under 60g for PLA.