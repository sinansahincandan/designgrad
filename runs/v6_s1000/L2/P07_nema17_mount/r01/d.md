**Concept**: An L-shaped bracket consisting of a solid vertical face plate to mount the NEMA 17 motor and a horizontal base plate to secure it to the table at $z=0$.

**Main Features**:
- **Face Plate**: A solid block from $y=0$ to $y=4$. It contains a central shaft bore and four M3 mounting holes. The face plate is designed to be a continuous solid before hole subtractions to ensure R2 compliance.
- **Base Plate**: A horizontal slab with its bottom surface at exactly $z=0$. To satisfy the mass limit (R7), the base plate thickness and footprint are optimized to keep total volume below $48.3 \text{ cm}^3$ ($60\text{g} / 1.24\text{g/cm}^3$).
- **Motor Interface**: A specific subtraction volume is removed from the inner corner of the L-shape to provide clearance for the motor body: $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$.
- **Load Path**: Motor torque and axial loads are transferred through the face plate into the base plate, then via two vertical M5 screws into the table at $z=0$.

**Requirements Fulfillment**:
- R1: Created as a single continuous solid using boolean operations (union of plates minus holes and clearance pocket).
- R2: Face plate is a solid block from $y=0$ to $y=4$; all hole subtractions are performed on this solid volume to ensure material integrity around the central bore.
- R3: Central bore $\varnothing 22.5$ mm located at $(x=0, z=30)$ passing through the face plate along the Y-axis.
- R4: Four motor screw holes, $\varnothing 3.4$ mm, passing through the face plate along the Y-axis at $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- R5: Motor clearance is ensured by subtracting a volume defined by $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$.
- R6: Base plate includes two vertical $\varnothing 5.5$ mm holes (along the Z-axis) at $(x, y) = (\pm 25, 25)$, extending from the top of the base plate down to $z=0$.
- R7: Envelope is constrained to $-35 \le x \le 35$ and $z_{max} \le 55$. The base plate dimensions are tuned to ensure total mass $\le 60$ g (Volume $< 48.38 \text{ cm}^3$).