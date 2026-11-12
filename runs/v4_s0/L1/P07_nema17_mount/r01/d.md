**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses a subtractive approach from two primary blocks (the face plate and the base plate) to ensure structural integrity and compliance with motor clearance requirements.

**Main Features**:
- **Face Plate**: Located at $y \in [0, 4]$, containing the motor mounting holes and central bore. It stands vertically against the motor.
- **Base Plate**: Located at $z \in [0, 5]$, providing the mounting surface on the table ($z=0$). It extends along the Y-axis from $y=0$ to $y=55$.
- **Motor Clearance Pocket**: A specific subtraction volume defined by $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$ to ensure the NEMA 17 body does not interfere with the bracket.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction (where the plates meet at the $y=0$ and $z=0$ intersection) and then distributed through the base plate into the table via two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions to ensure one single valid solid.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$) with solid material maintained around the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$ through the face plate along the Y-axis.
- R4: Four motor holes $\varnothing 3.4$ mm at $(x, z) = (\pm 15.5, 30 \pm 15.5)$, passing through the face plate along the Y-axis.
- R5: Motor clearance is guaranteed by subtracting a volume spanning $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$.
- R6: Two base holes $\varnothing 5.5$ mm at $(x, y) = (\pm 25, 25)$ passing vertically through the base plate along the Z-axis.
- R7: Envelope is defined by $x \in [-25, 25]$, $y \in [0, 55]$, and $z \in [0, 55]$. This fits within the required $-35 \le x \le 35$ and $\text{top} \le 55$ mm. Given a base plate thickness of 5mm and face plate thickness of 4mm, the volume is calculated to be well under the 60g limit for PLA (density 1.24 g/cm³).