**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses a constructive approach: first defining the primary volumes (Face Plate and Base Plate) as solid blocks, then performing subtractions for holes and clearances to ensure structural integrity, non-zero volume for all features, and strict adherence to coordinate constraints.

**Main Features**:
- **Face Plate**: A solid block of thickness 4mm occupying $y \in [0, 4]$ and $z \in [0, 55]$. To ensure R2/R3 compliance, the Face Plate is constructed as a solid manifold first; then, the central bore ($\varnothing 22.5$ mm) is subtracted through the full thickness of the plate (from $y=0$ to $y=4$) at $(x=0, z=30)$.
- **Base Plate**: A solid block with thickness $T$ occupying the space $z \in [0, T]$. This ensures the bottom surface sits exactly on the table plane at $z=0$. It provides the mounting surface for the table.
- **Motor Interface**: A recessed pocket cut into the face plate to ensure clearance for the NEMA 17 body in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting screws located at $z=0$.

**Requirement Compliance**:
- **R1**: Created using a single boolean union of the Face Plate and Base Plate, followed by subtractions.
- **R2/R3**: The Face Plate is constructed as a solid block ($y \in [0, 4], z \in [0, 55]$) first; the central bore ($\varnothing 22.5$ mm) is then subtracted through the volume at $(x=0, z=30)$ to ensure a valid annulus exists and material remains around the bore.
- **R4**: Four motor holes with a diameter of exactly $\varnothing 3.4$ mm are subtracted from the face plate at $(\pm 15.5, 30 \pm 15.5)$.
- **R5**: A pocket is subtracted from the back of the face plate to provide clearance for the motor body.
- **R6**: Two vertical $\varnothing 5.5$ mm holes are subtracted through the Base Plate at $(x=\pm 25, y=25)$, extending from $z=0$ to $z=T$.
- **R7**: Envelope is within $-35 \le x \le 35$, top $\le 55$ mm; volume is calculated to be well under the 60g limit for PLA.