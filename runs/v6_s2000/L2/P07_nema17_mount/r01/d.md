**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the motor and a horizontal base plate to secure it to the table. The design uses a "pocketed" approach to minimize mass while maintaining structural rigidity around screw holes.

**Main Features**:
- **Face Plate**: 4mm thick, positioned from $y=0$ to $y=4$. Contains a large central bore and four M3 mounting holes.
- **Base Plate**: Extends from the face plate into the $+Y$ region, resting on the table at $z=0$.
- **Motor Interface**: A recessed area ensures the motor body (42.3mm square) fits without interference in the $-Y$ region.
- **Fasteners**: 
    - Four $\varnothing 3.4$ mm holes at $(x, z) = (\pm 15.5, 30 \pm 15.5)$ passing through the face plate along the Y-axis.
    - Two $\varnothing 5.5$ mm holes at $(x, y) = (\pm 25, 25)$ oriented vertically (along the Z-axis) in the base plate.

**Load Path**: Motor torque and axial thrust are transferred through the face plate (holes along Y) to the base plate, which distributes the load into the table via the two vertical M5 screw locations (holes along Z).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Face plate thickness is 4mm ($y \in [0, 4]$) with material around the bore.
- R3: Central bore of $\varnothing 22.5$ mm centered at $(x=0, z=30)$ passing through the entire face plate thickness ($y \in [0, 4]$).
- R4: Four $\varnothing 3.4$ mm holes at $(x, z) = (\pm 15.5, 30 \pm 15.5)$ passing through the face plate along the Y-axis.
- R5: A large cutout is subtracted from the face plate to ensure motor clearance in the specified volume ($-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$).
- R6: Base plate includes two $\varnothing 5.5$ mm vertical holes at $(x, y) = (\pm 25, 25)$ oriented along the Z-axis.
- R7: Envelope fits within $x \in [-35, 35]$ and $z_{max} < 55$; mass is optimized via pocketing to stay under 60g.