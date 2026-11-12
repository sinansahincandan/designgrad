**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the motor and a horizontal base plate to secure it to the table. The design uses localized material removal (pockets) in non-load-bearing areas between mounting holes to minimize mass, ensuring all screw hole perimeters and the central bore remain fully encased in solid material.

**Main Features**:
- **Face Plate**: 4mm thick ($y \in [0, 4]$), positioned at the motor interface. Ensure a minimum wall thickness of 2mm between any hole edge and the boundary of the face plate or adjacent holes to maintain structural integrity.
- **Base Plate**: Extends from the face plate into the $+Y$ region, resting on the table at $z=0$.
- **Motor Interface**: A recessed area (subtracted volume) ensures the motor body (42.3mm square) fits without interference in the specified clearance zone.
- **Fasteners (Subtractive Operations)**:
    - **Central Bore (R3)**: A $\varnothing 22.5$ mm cylindrical hole subtracted from the face plate, centered at $(0, y, 30)$.
    - **Motor Holes (R4)**: Four $\varnothing 3.4$ mm cylindrical holes subtracted through the face plate along the Y-axis at $(\pm 15.5, 30 \pm 15.5)$.
    - **Table Mounting Holes (R6)**: Two $\varnothing 5.5$ mm cylindrical holes subtracted vertically through the base plate (oriented in the Z direction) at $(x, y) = (\pm 25, 25)$.

**Load Path**: Motor torque and axial thrust are transferred through the face plate to the base plate, which distributes the load into the table via the two M5 screw locations.

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Face plate thickness is 4mm ($y \in [0, 4]$) with solid material around the bore and maintaining a minimum 2mm wall thickness from all edges/holes.
- R3: Central bore of $\varnothing 22.5$ mm subtracted through the face plate at $(0, y, 30)$.
- R4: Four $\varnothing 3.4$ mm holes subtracted through the face plate along the Y-axis at $(\pm 15.5, 30 \pm 15.5)$.
- R5: A large cutout is subtracted from the face plate to ensure motor clearance in the specified volume ($-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$).
- R6: Base plate includes two $\varnothing 5.5$ mm holes subtracted vertically in the Z direction at $(\pm 25, 25)$.
- R7: Envelope fits within $x \in [-35, 35]$ and $z_{max} < 55$; mass is optimized via localized pocketing in non-load-bearing areas to stay under 60g.