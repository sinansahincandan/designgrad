**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined by a fillet to ensure structural integrity. The design uses a subtractive approach from two primary blocks to ensure a single solid manifold.

**Main Features**:
- **Face Plate**: Located at $y \in [0, 4]$, containing the motor mounting holes and central bore. This is a solid volume where all specified holes are modeled as through-holes via Boolean Subtractions.
- **Base Plate**: Occupies the plane $z=0$ as its bottom surface, extending to $z=5$. It provides the mounting surface for the table.
- **Motor Interface**: A recessed area (pocket) to accommodate the NEMA 17 body while maintaining screw alignment.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions to ensure one single valid solid.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$) with solid material maintained around the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$ through the face plate. This must be modeled as a cylinder primitive with a height of at least 4mm (spanning $y=0$ to $y=4$) and subtracted from the face plate volume using a Boolean Subtraction to ensure a $0\%$ walled ratio.
- R4: Four motor holes $\varnothing 3.4$ mm must be modeled as cylinders and subtracted from the face plate volume along the Y-axis (from $y=0$ to $y=4$). The holes are located at $(x, z)$ coordinates: $(15.5, 45.5)$, $(15.5, 14.5)$, $(-15.5, 45.5)$, and $(-15.5, 14.5)$.
- R5: A pocket is cut into the back of the face plate (negative Y space) to ensure clearance for the motor body within the specified volume.
- R6: Two base holes $\varnothing 5.5$ mm at $(x, y) = (\pm 25, 25)$ passing through the base plate along the Z-axis.
- R7: Envelope is approx. $50 \times 50 \times 55$ mm; volume is calculated to be well under the 60g limit for PLA.