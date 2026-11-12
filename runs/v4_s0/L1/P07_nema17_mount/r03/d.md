**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses a subtractive approach from two primary blocks (the face plate and the base plate) to ensure structural integrity and compliance with motor clearance requirements.

**Main Features**:
- **Face Plate**: Located at $y \in [0, 4]$, containing the motor mounting holes and central bore. It stands vertically against the motor.
- **Base Plate**: Located at $z \in [0, 5]$, providing the mounting surface on the table ($z=0$). It extends along the Y-axis from $y=0$ to $y=55$ and along the X-axis from $x=-30$ to $x=30$.
- **Motor Clearance Pocket**: A specific subtraction volume defined by $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$ to ensure the NEMA 17 body does not interfere with the bracket.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction (where the plates meet at the $y=0$ and $z=0$ intersection) and then distributed through the base plate into the table via two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions to ensure one single valid solid.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$) with solid material maintained around the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$ through the face plate along the Y-axis.
- R4: Four motor holes $\varnothing 3.4$ mm at $(x, z) = (\pm 15.5, 30 \pm 15.5)$, passing through the face plate along the Y-axis.
- R5: Motor clearance is guaranteed by subtracting a volume spanning $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$.
- R6: Two base holes $\varnothing 5.5$ mm at $(x, y) = (\pm 25, 25)$ passing vertically through the base plate along the Z-axis. These are contained within the expanded base plate width ($x \in [-30, 30]$), providing a 5mm margin from the edges.
- R7: Envelope is defined by $x \in [-30, 30]$, $y \in [0, 55]$, and $z \in [0, 55]$. This fits within the required $-35 \le x \le 35$ and $\text{top} \le 55$ mm. 
  *Mass Estimation*: The volume of the base plate ($60 \times 55 \times 5 = 16,500\text{ mm}^3$) plus face plate ($4 \times 55 \times 60 = 13,200\text{ mm}^3$) minus subtractions is approximately $28,000\text{ mm}^3$. At a density of $1.24\text{ g/cm}^3$ (or $0.00124\text{ g/mm}^3$), the mass is approximately $34.7\text{ g}$, which is well under the 60g limit.