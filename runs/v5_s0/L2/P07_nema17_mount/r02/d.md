**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses a constructive approach: first defining the primary volumes (Face Plate and Base Plate) as solid blocks, then performing subtractions for holes and clearances to ensure structural integrity and non-zero volume for all features.

**Main Features**:
- **Face Plate**: A solid block with dimensions $x \in [-35, 35]$, $y \in [0, 4]$, and $z \in [0, 55]$. This width ensures sufficient material remains around the central bore to satisfy R2.
- **Base Plate**: A solid block occupying $x \in [-35, 35]$, $y \in [0, 25]$, and $z \in [0, T]$ (where $T = 5$ mm). The base plate is joined to the face plate via a boolean union at the interface where their volumes overlap.
- **Central Bore**: A cylinder subtraction of $\varnothing 22.5$ mm with its axis passing through $(x=0, z=30)$, extending from $y=0$ to $y=4$.
- **Motor Holes**: Four cylinders of $\varnothing 3.4$ mm with axes passing through $(x, z) = (15.5, 45.5), (15.5, 14.5), (-15.5, 45.5),$ and $(-15.5, 14.5)$, extending along the Y-axis from $y=0$ to $y=4$.
- **Motor Interface**: A recessed pocket subtraction in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, and $8.5 \le z \le 51.5$ to provide clearance for the NEMA 17 body.
- **Base Mounting Holes**: Two cylinders of $\varnothing 5.5$ mm with axes passing through $(x, y) = (25, 25)$ and $(-25, 25)$, extending vertically along the Z-axis from $z=0$ to $z=T$.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws located at $z=0$.

**Requirement Compliance**:
- R1: Created using a single boolean union of the Face Plate and Base Plate, followed by subtractions.
- R2/R3: The Face Plate is constructed as a solid manifold ($x \in [-35, 35]$) first; the central bore ($\varnothing 22.5$ mm) is then subtracted through the volume at $(0, 30)$ to ensure a valid annulus exists with material remaining on all sides.
- R4: Four motor holes $\varnothing 3.4$ mm are subtracted from the face plate along the Y-axis at the specified $(x, z)$ coordinates.
- R5: A pocket is subtracted from the $y < 0$ side of the face plate to provide clearance for the motor body.
- R6: Two base holes $\varnothing 5.5$ mm are subtracted vertically through the base plate thickness $T$ at $(x, y) = (\pm 25, 25)$.
- R7: Envelope is within $-35 \le x \le 35$, top $\le 55$ mm; with $T=5$ mm, the volume is calculated to be well under the 60g limit for PLA.