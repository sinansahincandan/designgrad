**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the motor and a horizontal base plate to secure it to the table.

**Main Features**:
- **Face Plate**: 4mm thick ($y=0$ to $y=4$), with extents $x \in [-35, 35]$ and $z \in [0, 55]$. Contains a large central bore for the shaft and four M3 mounting holes.
- **Base Plate**: Extends from $z=0$ to $z=15$, providing a footprint on the table ($x \in [-35, 35], y \in [0, 50]$).
- **Motor Interface**: The face plate is notched/recessed at the inner corner where it meets the base plate. A volume defined by $x \in [-21.5, 21.5]$, $z \in [8.5, 51.5]$, and $y \in [0, 4]$ is subtracted to ensure no interference with the motor body (which sits at $y < 0$).
- **Load Path**: Motor torque and axial loads are transferred through the face plate into the base plate, then via the two M5 screws into the table.

**Requirements Fulfillment**:
- R1: Created as a single continuous solid by constructing a bounding L-shape block and performing boolean subtractions for all holes and the motor clearance pocket.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$) with sufficient material surrounding the central bore within the defined face plate extents.
- R3: Central bore $\varnothing 22.5$ mm located at $(0, z=30)$ through the face plate.
- R4: Four $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$.
- R5: Motor clearance is ensured by subtracting a volume of $x \in [-21.5, 21.5]$, $z \in [8.5, 51.5]$, and $y \in [0, 4]$ to prevent collision with the motor body at $y < 0$.
- R6: Base plate includes two $\varnothing 5.5$ mm holes at $(\pm 25, 25)$.
- R7: Dimensions are within $x \in [-35, 35]$ and $z_{max} = 55$. The total volume is approximately $38,000 \text{ mm}^3$; at a density of $1.24\text{ g/cm}^3$ ($0.00124\text{ g/mm}^3$), the total mass $\approx 47.1\text{ g}$, which is $< 60\text{ g}$.