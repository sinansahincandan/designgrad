**Concept**: An L-shaped bracket consisting of a vertical face plate (occupying $y \in [0, 4]$) and a horizontal base plate (sitting on the table at $z=0$ and extending in the $+Z$ direction), joined to form a single solid manifold. The design uses a subtractive approach from two primary blocks to ensure structural integrity and compliance with motor clearance requirements.

**Main Features**:
- **Face Plate**: A vertical plate located at $y \in [0, 4]$, centered on the motor shaft axis $(x=0, z=30)$.
- **Base Plate**: A horizontal plate resting on the table ($z=0$), extending upwards in the $+Z$ direction to provide a mounting surface.
- **Motor Interface**: A recessed pocket/clearance zone to accommodate the NEMA 17 body (located in $y < 0$) while ensuring screw alignment and shaft clearance.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via two vertical M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions to ensure one valid solid.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$), with solid material maintained around the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$, passing through the face plate along the Y-axis.
- R4: Four motor holes $\varnothing 3.4$ mm passing through the face plate along the Y-axis at $(\pm 15.5, 45.5)$ and $(\pm 15.5, 14.5)$.
- R5: A clearance volume is subtracted to ensure no material exists in $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$.
- R6: Two base holes $\varnothing 5.5$ mm located at $(x, y) = (\pm 25, 25)$, passing vertically through the base plate along the Z-axis.
- R7: Envelope is within $-35 \le x \le 35$, top $\le 55$ mm; volume is calculated to be well under the 60g limit for PLA.