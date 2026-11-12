**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined by a fillet to ensure structural integrity. The design uses a subtractive approach from two primary blocks to ensure a single solid manifold.

**Main Features**:
- **Face Plate**: Located at $y \in [0, 4]$, containing the motor mounting holes and central bore.
- **Base Plate**: Located at $z \in [0, 5]$, providing the mounting surface for the table.
- **Motor Interface**: A recessed area to accommodate the NEMA 17 body while maintaining screw alignment.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$).
- R3: Central bore $\varnothing 22.5$ mm centered at $(0, 30)$ through the face plate.
- R4: Four motor holes $\varnothing 3.4$ mm at $(\pm 15.5, 30 \pm 15.5)$.
- R5: A pocket is cut into the back of the face plate to ensure clearance for the motor body.
- R6: Two base holes $\varnothing 5.5$ mm at $(\pm 25, 25)$ in the $z=0$ plane.
- R7: Envelope is approx. $50 \times 50 \times 55$ mm; volume is calculated to be well under the 60g limit for PLA.