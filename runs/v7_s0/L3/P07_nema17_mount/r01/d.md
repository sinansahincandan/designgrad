**Concept**: An L-shaped bracket formed by a base plate sitting on the $z=0$ plane (the table) and a vertical face plate rising from the $y=0$ plane. The design ensures the part occupies the $+Y$ and $+Z$ octants, with the motor pressing against the face plate from the $-Y$ side. The geometry is constructed as a single solid manifold using subtractive operations from primary blocks to ensure structural integrity and compliance with R1.

**Main Features**:
- **Face Plate**: A vertical plate located at $y \in [0, 4]$, providing the mounting surface for the motor.
- **Base Plate**: A horizontal plate located at $z \in [0, 5]$, providing the mounting surface on the table ($z=0$).
- **Motor Interface**: Four cylindrical through-holes and a central bore designed to accommodate a NEMA 17 stepper motor.

**Load Path**: The motor's reaction force is applied against the face plate at $y=0$, transferred through the $y \in [0, 4]$ thickness into the corner junction, and distributed through the base plate ($z \in [0, 5]$) into the table via two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions to ensure one valid solid.
- R2: Face plate thickness is strictly constrained to $y \in [0, 4]$ with solid material maintained around the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$, passing through the face plate from $y=4$ to $y=0$.
- R4: Four motor screw holes $\varnothing 3.4$ mm, cylindrical through-holes passing through the face plate along the Y-axis, located at $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- R5: A clearance volume is subtracted to ensure no material exists in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, and $8.5 \le z \le 51.5$.
- R6: Two base holes $\varnothing 5.5$ mm located at $(x, y) = (\pm 25, 25)$ on the $z=0$ plane.
- R7: Envelope is constrained within $-35 \le x \le 35$, $y_{max} \approx 50$ (implied by plate dimensions), and $z \le 55$ mm; volume is calculated to ensure mass $\le 60$ g using PLA density.