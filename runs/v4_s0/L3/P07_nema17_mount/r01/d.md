**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses a subtractive approach from two primary blocks (Face Plate and Base Plate) to ensure R1 compliance.

**Main Features**:
- **Face Plate**: A solid block occupying $y \in [0, 4]$. It serves as the mounting surface for the NEMA 17 motor. To satisfy R2, this volume is established before any holes are drilled.
- **Base Plate**: A solid block sitting on the table ($z=0$). Its thickness extends from $z=0$ to a positive height (e.g., $z \in [0, 10]$) to provide a stable mounting surface for the bracket.
- **Motor Interface (R5)**: A clearance pocket is subtracted from the geometry to accommodate the motor body in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, and $8.5 \le z \le 51.5$.

**Load Path**: The motor's reaction force is applied at the face plate ($y=0$), transferred through the $y \in [0, 4]$ thickness into the corner junction, and distributed through the base plate into the table via two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the Face Plate and Base Plate, followed by subtractions for holes and clearance.
- R2: Face plate thickness is strictly $4\text{ mm}$ ($y=0$ to $y=4$), ensuring solid material remains around all bores.
- R3: Central bore $\varnothing 22.5\text{ mm}$ is centered at $(x=0, z=30)$ and passes through the face plate along the Y-axis.
- R4: Four motor holes $\varnothing 3.4\text{ mm}$ are located at $(\pm 15.5, 30 \pm 15.5)$ on the face plate.
- R5: A clearance volume is subtracted to ensure no material interferes with the NEMA 17 body in the specified $x, y, z$ range.
- R6: Two base holes $\varnothing 5.5\text{ mm}$ are located at $(x, y) = (\pm 25, 25)$ and pass through the base plate to the table ($z=0$).
- R7: Envelope is constrained within $-35 \le x \le 35$ and $z_{max} \le 55\text{ mm}$; mass is optimized to stay under $60\text{ g}$ using PLA density.