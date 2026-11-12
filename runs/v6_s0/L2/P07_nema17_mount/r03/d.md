**Concept**: An L-shaped bracket formed by the boolean union of two primary rectangular prisms: a face plate ($x \in [-35, 35], y \in [0, 4], z \in [0, 55]$) and a base plate. This ensures a single solid manifold with a continuous 4mm thickness for the face plate before any features are subtracted.

**Main Features**:
- **Face Plate**: A solid rectangular prism defined by $y \in [0, 4]$, serving as the mounting surface for the motor.
- **Base Plate**: A horizontal component resting on the table ($z=0$), providing the mounting surface for the bracket itself.
- **Motor Interface**: A recessed pocket to ensure clearance for the NEMA 17 body.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via two vertical M5 mounting screws.

**Requirement Compliance**:
- **R1/R2**: Created by performing a `union()` of a solid face plate block ($x \in [-35, 35], y \in [0, 4], z \in [0, 55]$) and the base plate, ensuring R2 thickness is maintained.
- **R3 (Central Bore)**: A `cut()` operation using a $\varnothing 22.5$ mm cylinder centered at $(0, y, 30)$ extending through the face plate from $y=0$ to $y=4$.
- **R4 (Motor Holes)**: Four `cut()` operations using $\varnothing 3.4$ mm cylinders located at $(\pm 15.5, y, 30 \pm 15.5)$, extending through the face plate along the Y-axis.
- **R5 (Motor Clearance)**: A `cut()` operation of a rectangular volume defined by $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, and $8.5 \le z \le 51.5$ to accommodate the motor body.
- **R6 (Base Holes)**: Two `cut()` operations using $\varnothing 5.5$ mm cylinders located at $(x, y) = (\pm 25, 25)$, oriented along the Z-axis, passing through the base plate to the table surface ($z=0$).
- **R7**: Envelope is within $-35 \le x \le 35$, $z \le 55$ mm; mass is calculated to be under the 60g limit for PLA.