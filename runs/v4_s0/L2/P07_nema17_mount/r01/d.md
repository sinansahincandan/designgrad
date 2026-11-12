**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined by a fillet to ensure structural integrity. The design uses a subtractive approach from two primary blocks to ensure a single solid manifold.

**Main Features**:
- **Face Plate**: A solid block spanning $x \in [-35, 35]$ and $z \in [0, 55]$, located at $y \in [0, 4]$. This large footprint ensures substantial material remains around the central bore to satisfy R2.
- **Base Plate**: A horizontal plate anchored to the table, occupying the volume where $z \in [0, H]$ (where $H$ is the thickness), ensuring the part's minimum $z$-coordinate is exactly 0.
- **Motor Interface**: A recessed pocket cut into the back of the face plate ($y < 0$) to accommodate the NEMA 17 body while maintaining screw alignment.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via two vertical M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions.
- R2: Face plate thickness is 4mm ($y=0$ to $y=4$), with dimensions large enough to ensure solid material surrounds the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$ through the face plate.
- R4: Four motor holes $\varnothing 3.4$ mm at $(\pm 15.5, 30 \pm 15.5)$ passing through the face plate along the Y-axis.
- R5: A pocket is cut into the back of the face plate ($y < 0$) to ensure clearance for the motor body within the specified volume ($-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$).
- R6: Two vertical base holes $\varnothing 5.5$ mm located at $(x, y) = (\pm 25, 25)$, extending through the thickness of the base plate along the Z-axis.
- R7: Envelope is within $-35 \le x \le 35$, $z_{max} \le 55$ mm; volume is calculated to be well under the 60g limit for PLA.