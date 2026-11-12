**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses a constructive approach: first defining the primary volumes (Face Plate and Base Plate) as solid blocks, then performing subtractions for holes and clearances to ensure structural integrity and non-zero volume for all features.

**Main Features**:
- **Face Plate**: A solid block of thickness 4mm occupying $y \in [0, 4]$ and $z \in [0, 55]$. The central bore ($\varnothing 22.5$ mm) and motor holes are defined as subtractions from this solid volume at $(x=0, z=30)$.
- **Base Plate**: A solid block of thickness $T$ occupying the space $z \in [0, T]$, ensuring the bottom surface sits exactly on the table plane at $z=0$. The two mounting holes are subtracted vertically along the Z-axis at $(x=\pm 25, y=25)$.
- **Motor Interface**: A recessed pocket cut into the face plate to ensure clearance for the NEMA 17 body in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, $8.5 \le z \le 51.5$.
- **Motor Holes (R4)**: Four cylindrical voids, each with a diameter of exactly $3.4$ mm and an infinite length along the Y-axis, are subtracted from the Face Plate at $(\pm 15.5, 30 \pm 15.5)$.
- **Base Holes (R6)**: Two cylindrical voids, each with a diameter of exactly $5.5$ mm, are subtracted from the Base Plate at $(x=\pm 25, y=25)$ extending through the full thickness $T$ along the Z-axis.

**Load Path**: The motor's reaction force is transferred through the face plate into the corner junction and then distributed through the base plate into the table via the two M5 mounting holes at $z=0$. Note: The motor screw holes (R4) and base mounting holes (R6) are voids within the solid manifold, not physical fasteners.

**Requirement Compliance**:
- R1: Created using a single boolean union of the Face Plate and Base Plate, followed by subtractions.
- R2/R3: The central bore must be a cylinder with diameter $22.5$ mm centered at $(x=0, z=30)$, passing through the Face Plate from $y=0$ to $y=4$. The subtraction must leave a minimum wall thickness of $1.75$ mm at the narrowest point (calculated as $[(z_{max} - z_{min})/2] - [radius]$) to ensure R2 compliance and that a valid annulus exists.
- R4: Four cylindrical voids $\varnothing 3.4$ mm are subtracted from the face plate along the Y-axis at $(\pm 15.5, 30 \pm 15.5)$.
- R5: A pocket is subtracted from the back of the face plate to provide clearance for the motor body.
- R6: Two cylindrical voids $\varnothing 5.5$ mm are subtracted vertically through the base plate at $(\pm 25, 25)$ in the $z=0$ plane (extending through thickness $T$).
- R7: Envelope is within $-35 \le x \le 35$, top $\le 55$ mm; volume is calculated to be well under the 60g limit for PLA.