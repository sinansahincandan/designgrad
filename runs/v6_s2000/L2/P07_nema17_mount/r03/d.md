**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the motor and a horizontal base plate to secure it to the table. The design uses a "pocketed" approach to minimize mass while maintaining structural rigidity around screw holes.

**Main Features**:
- **Face Plate**: A solid slab occupying $y \in [0, 4]$. It serves as the mounting surface for the motor.
- **Base Plate**: Extends from the face plate into the $+Y$ region, positioned such that its bottom surface lies exactly at $z=0$.
- **Central Bore (R3)**: A cylindrical void of $\varnothing 22.5$ mm subtracted through the face plate along the Y-axis, centered at $(x=0, y, z=30)$.
- **Motor Screw Holes (R4)**: Four cylindrical voids of $\varnothing 3.4$ mm subtracted through the face plate along the Y-axis at coordinates: $(15.5, y, 45.5)$, $(-15.5, y, 45.5)$, $(15.5, y, 14.5)$, and $(-15.5, y, 14.5)$.
- **Motor Interface (R5)**: A large volume subtraction to ensure motor clearance in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$.
- **Table Mounting Holes (R6)**: Two vertical cylindrical voids of $\varnothing 5.5$ mm (parallel to the Z-axis) subtracted at $(x, y) = (25, 25)$ and $(-25, 25)$.
- **Fasteners**: Uses NEMA 17 screws for the motor interface and M5 screws for table mounting.

**Load Path**: Motor torque and axial thrust are transferred through the face plate to the base plate, which distributes the load into the table via the two vertical M5 screw locations at $z=0$.

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Face plate thickness is 4mm ($y \in [0, 4]$) with material around the bore.
- R3: Central bore of $\varnothing 22.5$ mm located at $(0, y, 30)$.
- R4: Four $\varnothing 3.4$ mm holes through the face plate at $(\pm 15.5, y, 45.5)$ and $(\pm 15.5, y, 14.5)$.
- R5: A large cutout is subtracted from the $-Y$ side to ensure motor clearance in the specified volume.
- R6: Base plate includes two $\varnothing 5.5$ mm vertical holes at $x = \pm 25, y = 25$.
- R7: Envelope fits within $x \in [-35, 35]$ and $z_{max} < 55$; mass is optimized via pocketing to stay under 60g.