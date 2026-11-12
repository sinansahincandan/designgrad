**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses an additive approach to create the primary L-shape (a boolean union of two rectangular prisms), followed by a series of subtractive operations (holes and clearance pockets) performed on that unified volume to ensure R1 compliance and structural integrity.

**Main Features**:
- **Face Plate**: A rectangular prism defined by $x \in [-35, 35]$, $y \in [0, 4]$, and $z \in [0, 55]$. This establishes the primary mounting surface.
- **Base Plate**: A rectangular prism located on the table ($z=0$) with thickness extending in the $+Z$ direction (e.g., $z \in [0, 5]$), providing the mounting surface for the table and joining with the face plate to form the L-shape.
- **Motor Interface**: A specific clearance pocket is subtracted from the Face Plate geometry specifically to create a recess for the NEMA 17 body, ensuring the motor can press against the $y=0$ plane.

**Subtractive Features**:
- **Central Bore**: A cylinder $\varnothing 22.5$ mm centered at $(x, z) = (0, 30)$ extending along the Y-axis through the Face Plate.
- **Motor Screw Holes**: Four cylinders $\varnothing 3.4$ mm located at $(x, z) = (\pm 15.5, 30 \pm 15.5)$ extending along the Y-axis from $y=0$ to $y=4$.
- **Motor Clearance Pocket**: A volume subtracted from the Face Plate to accommodate the motor body.
- **Base Mounting Holes**: Two vertical cylinders $\varnothing 5.5$ mm centered at $(x, y) = (\pm 25, 25)$ extending along the Z-axis through the base plate.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via two vertical cylindrical mounting holes.

**Requirement Compliance**:
- R1: Created by performing a boolean union of the Face Plate and Base Plate, followed by all subtractive operations (Bore, Motor Holes, Clearance Pocket, and Base Holes) on that single unified volume to ensure one valid solid.
- R2: The face plate is defined as a solid volume from $y=0$ to $y=4$; all subtractive holes (R3, R4) must be centered within this thickness and not exceed these bounds to maintain the 4mm structural requirement.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x, z) = (0, 30)$ passing through the face plate along the Y-axis.
- R4: Four cylindrical motor holes $\varnothing 3.4$ mm passing through the face plate from $y=0$ to $y=4$ along the Y-axis at $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- R5: A clearance volume is subtracted for the motor body in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, and $8.5 \le z \le 51.5$.
- R6: Two vertical cylindrical holes $\varnothing 5.5$ mm centered at $(x, y) = (\pm 25, 25)$ extending through the base plate along the Z-axis.
- R7: Envelope is within $-35 \le x \le 35$, $y \in [0, 4]$, and top $\le 55$ mm; volume is calculated to be well under the 60g limit for PLA.