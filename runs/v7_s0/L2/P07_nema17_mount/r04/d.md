**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined by a fillet to ensure structural integrity. The design uses a subtractive approach from two primary blocks to ensure a single solid manifold.

**Main Features**:
- **Face Plate**: Located at $y \in [0, 4]$, containing the motor mounting holes and central bore. This is a solid volume where all specified holes are modeled as through-holes via subtraction.
- **Base Plate**: Occupies the plane $z=0$ as its bottom surface, extending to $z=5$. It provides the mounting surface for the table.
- **Motor Interface**: A recessed area (pocket) to accommodate the NEMA 17 body while maintaining screw alignment.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by explicit `cut` operations to ensure one single valid solid manifold.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$) with solid material maintained around the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$. This must be implemented as a subtraction of a cylinder extending through the entire thickness of the face plate along the Y-axis (from $y=0$ to $y=4$).
- R4: Four motor holes $\varnothing 3.4$ mm centered at $(x, z) \in \{(\pm 15.5, 45.5), (\pm 15.5, 14.5)\}$. These must be implemented as subtractions of cylinders through the face plate along the Y-axis (from $y=0$ to $y=4$).
- R5: A pocket is cut into the back of the face plate (negative Y space) to ensure clearance for the motor body within the specified volume: $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$.
- R6: Two base holes $\varnothing 5.5$ mm centered at $(x, y) = (\pm 25, 25)$. These must be implemented as subtractions of cylinders through the base plate along the Z-axis (from $z=0$ to $z=5$).
- R7: Envelope is approx. $50 \times 50 \times 55$ mm; volume is calculated to be well under the 60g limit for PLA.

**Boolean Logic Mandate**: To ensure all holes are correctly registered as empty space, every hole (R3, R4, and R6) must be performed using a formal `cut` or `subtraction` operation against the primary L-shape manifold.