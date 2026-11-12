**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined by a fillet to ensure structural integrity. The design uses a subtractive approach from two primary blocks (one for the face plate in $y \in [0, 4]$ and one for the base plate at $z \in [0, 5]$) to ensure a single solid manifold.

**Main Features**:
- **Face Plate**: Positioned with its mounting surface at $y=0$, extending into the positive Y direction ($y \in [0, 4]$). It contains the motor mounting holes and central bore.
- **Base Plate**: Located on the table surface ($z=0$), extending upwards in the Z direction to a thickness of 5mm ($z \in [0, 5]$). The plate extends in the X and Y directions such that the mounting points at $(x, y) = (\pm 25, 25)$ are contained within its footprint.
- **Motor Interface**: A recessed area/pocket cut into the face plate at $y \in [0, 4]$ to accommodate the NEMA 17 body (which occupies $y < 0$) while maintaining screw alignment.
- **Base Mounting Holes**: Two $\varnothing 5.5$ mm holes drilled vertically through the entire thickness of the base plate ($z=0$ to $z=5$) at $(x, y) = (\pm 25, 25)$.

**Load Path**: The motor's reaction force is transferred through the face plate (at $y=0$) into the corner junction and then distributed through the base plate (at $z=0$) into the table via the two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions to ensure one single valid solid.
- R2: Face plate is a continuous solid from $y=0$ to $y=4$. The central bore (R3) and motor holes (R4) are performed as subtractions from this 4mm thick volume, ensuring material remains around the bores.
- R3: Central bore diameter is exactly **22.5 mm** centered at $(x=0, z=30)$ passing through the face plate along the Y-axis.
- R4: Four motor holes $\varnothing 3.4$ mm passing through the face plate along the Y-axis, located at $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- R5: A pocket is cut into the face plate to ensure clearance for the motor body in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$.
- R6: Two base holes $\varnothing 5.5$ mm are drilled vertically through the entire thickness of the base plate at $(x, y) = (\pm 25, 25)$.
- R7: Envelope is within $-35 \le x \le 35$, top $\le 55$ mm; volume is calculated to be well under the 60g limit for PLA.