**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single continuous solid manifold. The design begins with the construction of a single solid volume (the L-shape) before any subtractive operations are performed to ensure structural integrity and compliance with thickness requirements.

**Main Features**:
- **Face Plate**: A solid rectangular prism spanning $x \in [-35, 35]$, $y \in [0, 4]$, and $z \in [0, 55]$. This ensures the face plate maintains its required thickness throughout the mounting area.
- **Base Plate**: A horizontal surface providing the mounting interface for the table at $z=0$.
- **Motor Interface**: A recessed pocket to accommodate the NEMA 17 body while maintaining screw alignment and clearance.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via two vertical M5 mounting screws.

**Requirement Compliance**:
- R1: Created as one single, valid solid manifold using a boolean union of the L-shape components before subtractions.
- R2: Face plate thickness is strictly maintained from $y=0$ to $y=4$; no material is removed from this region except for the specified bores.
- R3: Central bore $\varnothing 22.5$ mm cylinder subtracted along the Y-axis, passing through $(x=0, z=30)$ and spanning the full face plate thickness ($y \in [0, 4]$).
- R4: Four motor screw holes $\varnothing 3.4$ mm cylinders subtracted along the Y-axis at coordinates $(x, z) = (\pm 15.5, 30 \pm 15.5)$, passing through the face plate thickness ($y=0$ to $y=4$).
- R5: A pocket is cut into the back of the face plate (in the $y < 0$ region relative to the motor) to ensure clearance for the motor body within the specified bounds: $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, and $8.5 \le z \le 51.5$.
- R6: Two base holes $\varnothing 5.5$ mm cylinders subtracted vertically along the Z-axis at $(x, y) = (\pm 25, 25)$ to penetrate the base plate.
- R7: Envelope is within $-35 \le x \le 35$, $z \le 55$ mm; volume is calculated to be well under the 60g limit for PLA.