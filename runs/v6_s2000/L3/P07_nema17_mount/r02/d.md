**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the motor and a horizontal base plate to secure it to the table. The design utilizes an "orthogonal pocketing" approach, subtracting rectangular volumes from the main body to minimize mass while maintaining a minimum 3mm wall thickness around all fastener locations to ensure structural integrity.

**Main Features**:
- **Face Plate**: 4mm thick ($y \in [0, 4]$), with a maximum height of $z=54$ mm to satisfy envelope constraints. It contains one central through-bore and four motor screw through-holes.
- **Base Plate**: Extends from the face plate into the $+Y$ region, resting on the table at $z=0$. It contains two vertical mounting through-holes.
- **Motor Interface**: A specific rectangular volume is subtracted from the face plate to ensure motor clearance in the specified volume ($-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$).
- **Fasteners (All through-holes)**: 
    - Four $\varnothing 3.4$ mm holes for NEMA 17 screws passing through the face plate along the Y-axis at $(\pm 15.5, 30 \pm 15.5)$.
    - One $\varnothing 22.5$ mm central bore passing through the face plate along the Y-axis at $(0, y, 30)$.
    - Two $\varnothing 5.5$ mm holes for M5 table mounting screws passing through the base plate along the Z-axis at $(\pm 25, 25)$.

**Load Path**: Motor torque and axial thrust are transferred through the face plate to the base plate, which distributes the load into the table via the two vertical M5 screw locations.

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean subtraction of holes and pockets from a primary block.
- R2: Face plate thickness is 4mm ($y \in [0, 4]$) with solid material maintained around all bores.
- R3: Central through-bore of $\varnothing 22.5$ mm located at $(0, y, 30)$.
- R4: Four $\varnothing 3.4$ mm through-holes at $(\pm 15.5, 30 \pm 15.5)$ passing through the face plate along Y.
- R5: A rectangular cutout is subtracted from the face plate to ensure motor clearance in the specified volume.
- R6: Base plate includes two $\varnothing 5.5$ mm vertical through-holes at $(\pm 25, 25)$ passing through the base along Z.
- R7: Envelope fits within $x \in [-35, 35]$ and $z_{max} = 54$ mm; mass is optimized via orthogonal pocketing to stay under 60g while maintaining $\ge 3$mm material around holes.