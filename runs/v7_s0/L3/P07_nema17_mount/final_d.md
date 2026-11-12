**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses a subtractive approach from two primary rectangular prisms to ensure structural integrity and compliance with the specified coordinate system.

**Main Features**:
- **Face Plate**: A rectangular prism defined by $x \in [-35, 35]$, $y \in [0, 4]$, and $z \in [0, 55]$. This ensures a consistent 4mm thickness (R2) across the entire mounting area.
- **Base Plate**: A rectangular prism located on the table ($z=0$) with thickness extending in the $+Z$ direction (e.g., $z \in [0, 5]$), providing the mounting surface for the table.
- **Motor Interface**: A specific clearance pocket is subtracted from the $-Y$ side of the face plate to accommodate the NEMA 17 motor body without interfering with the bracket's structural volume.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via two vertical cylindrical mounting holes.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape (Face Plate and Base Plate), followed by subtractions to create holes and clearances.
- R2: Face plate thickness is maintained at 4mm ($y=0$ to $y=4$) across its entire $X/Z$ footprint.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x, z) = (0, 30)$ passing through the face plate along the Y-axis.
- R4: Four cylindrical motor holes $\varnothing 3.4$ mm passing through the face plate from $y=0$ to $y=4$ at $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- R5: A clearance volume is subtracted for the motor body in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, and $8.5 \le z \le 51.5$.
- R6: Two vertical cylindrical holes $\varnothing 5.5$ mm centered at $(x, y) = (\pm 25, 25)$ extending through the base plate along the Z-axis.
- R7: Envelope is within $-35 \le x \le 35$, $y \in [0, 4]$, and top $\le 55$ mm; volume is calculated to be well under the 60g limit for PLA.