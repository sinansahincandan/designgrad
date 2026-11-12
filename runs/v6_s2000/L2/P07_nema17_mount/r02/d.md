**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the motor and a horizontal base plate to secure it to the table. The design uses a "pocketed" approach to minimize mass while maintaining structural rigidity around screw holes.

**Main Features**:
- **Face Plate**: 4mm thick, positioned from $y=0$ to $y=4$. Contains a large central bore and four M3 mounting holes.
- **Base Plate**: Extends from the face plate into the $+Y$ region, resting on the table at $z=0$.
- **Motor Interface**: A recessed area ensures the motor body (42.3mm square) fits without interference.
- **Fasteners**: 
    - A cylinder of $\varnothing 22.5$ mm is subtracted from the face plate along the Y-axis, centered at $(x=0, z=30)$.
    - Four cylinders of $\varnothing 3.4$ mm are subtracted from the face plate along the Y-axis at $(\pm 15.5, 30 \pm 15.5)$.
    - Two cylinders of $\varnothing 5.5$ mm are subtracted from the base plate along the Z-axis at $(x=\pm 25, y=25)$.

**Load Path**: Motor torque and axial thrust are transferred through the face plate to the base plate, which distributes the load into the table via the two M5 screw locations.

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Face plate thickness is 4mm ($y \in [0, 4]$) with material around the bore.
- R3: A $\varnothing 22.5$ mm cylinder is subtracted from the face plate at $(0, y, 30)$.
- R4: Four $\varnothing 3.4$ mm cylinders are subtracted through the face plate along Y at $(\pm 15.5, 30 \pm 15.5)$.
- R5: A large cutout is subtracted from the face plate to ensure motor clearance in the specified volume.
- R6: Two $\varnothing 5.5$ mm cylinders are subtracted through the base plate along Z at $(x=\pm 25, y=25)$.
- R7: Envelope fits within $x \in [-35, 35]$ and $z_{max} < 55$; mass is optimized via pocketing to stay under 60g.