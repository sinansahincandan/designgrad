**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the motor and a horizontal base plate to secure it to the table.

**Main Features**:
- **Face Plate**: 4mm thick, positioned from $y=0$ to $y=4$. Contains a large central bore for the shaft and four M3 mounting holes.
- **Base Plate**: Extends from $z=0$ to $z \approx 15$, providing a footprint on the table ($x \in [-35, 35], y \in [0, 50]$).
- **Motor Interface**: The face plate is recessed/cut to ensure motor clearance.
- **Load Path**: Motor torque and axial loads are transferred through the face plate into the base plate, then via the two M5 screws into the table.

**Requirements Fulfillment**:
- R1: Created as a single continuous solid using boolean union of the L-shape minus the holes.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$).
- R3: Central bore $\varnothing 22.5$ mm located at $(0, z=30)$ through the face plate.
- R4: Four $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$.
- R5: A large pocket is subtracted from the inner corner to ensure no interference with the motor body ($x \in [-21.5, 21.5], y < 0$).
- R6: Base plate includes two $\varnothing 5.5$ mm holes at $(\pm 25, 25)$.
- R7: Dimensions are within $x \in [-35, 35]$ and $z_{max} = 55$; volume is calculated to be well under the mass limit for PLA.