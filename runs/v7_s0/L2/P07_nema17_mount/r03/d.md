**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined by a fillet to ensure structural integrity. The design uses a subtractive approach from two primary blocks to ensure a single solid manifold.

**Main Features**:
- **Face Plate**: Located at $y \in [0, 4]$, containing the motor mounting holes and central bore. This is a solid volume where all specified holes are modeled as through-holes. The central bore must be implemented using a `cut` operation (subtraction) from the face plate volume to ensure a zero-walled interior. Four $\varnothing 3.4$ mm through-holes must be subtracted from the face plate at exactly $(x, z) = (15.5, 45.5), (-15.5, 45.5), (15.5, 14.5),$ and $(-15.5, 14.5)$.
- **Base Plate**: Occupies the plane $z=0$ as its bottom surface, extending to $z=5$. It provides the mounting surface for the table.
- **Motor Interface**: A recessed area (pocket) to accommodate the NEMA 17 body while maintaining screw alignment.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws. All holes (R3, R4, R6) must be performed as boolean subtractions from the primary solid to ensure a single manifold without internal non-manifold edges or trapped volumes.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions to ensure one single valid solid.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$) with solid material maintained around the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$ through the face plate as a boolean subtraction of a cylinder extending through the entire thickness of the face plate along the Y-axis ($y \in [0, 4]$). No material should remain within the $r=11.25$ mm radius.
- R4: Four holes, diameter 3.4 mm, must be created by subtracting cylinders from the face plate volume. The cylinder axes must be parallel to the Y-axis, passing through the points $(x=15.5, z=45.5)$, $(x=-15.5, z=45.5)$, $(x=15.5, z=14.5)$, and $(x=-15.5, z=14.5)$.
- R5: A pocket is cut into the back of the face plate (negative Y space) to ensure clearance for the motor body within the specified volume.
- R6: Two base holes $\varnothing 5.5$ mm at $(x, y) = (\pm 25, 25)$ passing through the base plate along the Z-axis.
- R7: Envelope is approx. $50 \times 50 \times 55$ mm; volume is calculated to be well under the 60g limit for PLA.