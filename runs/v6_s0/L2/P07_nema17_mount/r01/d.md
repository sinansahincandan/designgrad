**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to ensure structural integrity. The design uses a subtractive approach starting from two primary solid blocks (a $70 \times 4 \times 60$ mm block for the face plate and a corresponding base block) to ensure a single solid manifold that satisfies all thickness requirements before holes are cut.

**Main Features**:
- **Face Plate**: A solid rectangular block defined by $x \in [-35, 35]$, $y \in [0, 4]$, and $z \in [0, 55]$.
- **Base Plate**: Located at $z \in [0, 5]$, providing the mounting surface for the table.
- **Motor Interface**: A recessed area to accommodate the NEMA 17 body while maintaining screw alignment.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the L-shape, followed by subtractions.
- R2: Face plate thickness is set to 4mm ($y=0$ to $y=4$) using a solid rectangular block as the starting volume.
- R3: Subtract a cylinder of $\varnothing 22.5$ mm centered at $(x=0, z=30)$ extending through the full thickness of the face plate ($y=0$ to $y=4$).
- R4: Subtract four cylinders of $\varnothing 3.4$ mm centered at $(x=\pm 15.5, z=30 \pm 15.5)$ extending through the face plate along the Y-axis ($y=0$ to $y=4$).
- R5: A pocket is cut into the back of the face plate to ensure clearance for the motor body (defined by $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$).
- R6: Subtract two vertical cylinders of $\varnothing 5.5$ mm centered at $(x=\pm 25, y=25)$ extending from the table surface ($z=0$) through the base plate.
- R7: Envelope is within $-35 \le x \le 35$, top $\le 55$ mm; volume is calculated to be well under the 60g limit for PLA.