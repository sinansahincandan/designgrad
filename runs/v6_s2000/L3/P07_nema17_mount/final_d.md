**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the motor and a horizontal base plate to secure it to the table. The design uses a "pocketed" approach to minimize mass while maintaining structural rigidity around screw holes.

**Main Features**:
- **Face Plate**: 4mm thick, positioned from $y=0$ to $y=4$. Contains a large central bore and four M3 mounting holes.
- **Base Plate**: Extends from the face plate into the $+Y$ region, resting on the table at $z=0$.
- **Motor Interface**: A recessed area ensures the motor body (42.3mm square) fits without interference.
- **Fasteners**: Four 3.4mm holes for NEMA 17 screws; two 5.5mm holes for M5 table mounting screws.

**Load Path**: Motor torque and axial thrust are transferred through the face plate to the base plate, which distributes the load into the table via the two M5 screw locations.

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Face plate thickness is 4mm ($y \in [0, 4]$) with material around the bore.
- R3: Central bore of $\varnothing 22.5$ mm located at $(0, 30)$.
- R4: Four $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$.
- R5: A large cutout is subtracted from the face plate to ensure motor clearance in the specified volume.
- R6: Base plate includes two $\varnothing 5.5$ mm holes at $(\pm 25, 25)$.
- R7: Envelope fits within $x \in [-35, 35]$ and $z_{max} < 55$; mass is optimized via pocketing to stay under 60g.