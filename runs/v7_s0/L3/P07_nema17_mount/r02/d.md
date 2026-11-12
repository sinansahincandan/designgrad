**Concept**: An L-shaped bracket where the base plate lies on $z \in [0, 5]$ (sitting on the table at $z=0$) and the face plate extends vertically from the base along the Y-axis at $y \in [0, 4]$. The design uses a subtractive approach from two primary blocks to ensure a single solid manifold.

**Main Features**:
- **Base Plate**: Located at $z \in [0, 5]$, providing the mounting surface for the table.
- **Face Plate**: A solid block of thickness 4mm located at $y \in [0, 4]$, perpendicular to the base plate, containing the motor mounting holes and central bore.
- **Motor Interface**: A clearance pocket is cut into the back of the face plate (the side facing $y < 0$) to accommodate the NEMA 17 body.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws located on the top surface of the base.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions.
- R2: Face plate thickness is strictly set to 4mm ($y=0$ to $y=4$), ensuring solid material remains around the central bore.
- R3: Central bore $\varnothing 22.5$ mm centered at $(x=0, z=30)$ through the face plate ($y \in [0, 4]$).
- R4: Four motor holes $\varnothing 3.4$ mm drilled through the face plate along the Y-axis at coordinates: $(15.5, 30), (-15.5, 30), (15.5, 45.5),$ and $(-15.5, 14.5)$.
- R5: A clearance pocket is cut to ensure no material exists in the volume $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$.
- R6: Two base holes $\varnothing 5.5$ mm located on the top surface of the base plate ($z=5$) at $(x, y) = (\pm 25, 25)$.
- R7: Envelope is within $-35 \le x \le 35$ and $z \le 55$ mm; volume is calculated to be well under the 60g limit for PLA.