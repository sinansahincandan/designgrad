**Concept**: An L-shaped bracket consisting of a vertical face plate and a horizontal base plate, joined to form a single solid manifold. The design uses a subtractive approach from two primary blocks (Face Plate and Base Plate) to ensure R1 compliance and geometric robustness.

**Main Features**:
- **Face Plate**: A continuous, solid block occupying $y \in [0, 4]$. This volume is established as a single unbroken mass before any holes or clearances are subtracted to satisfy the "solid material around all bores" requirement in R2.
- **Base Plate**: A solid block sitting on the table ($z=0$). Its thickness extends from $z=0$ to $z=15$ to provide a stable mounting surface and ensure sufficient depth for R6 mounting holes.
- **Corner Overlap Volume (Junction)**: To prevent thin-walled artifacts or unintended chamfers at the L-junction, the Face Plate and Base Plate intersect through a shared volume defined by $y \in [0, 4]$ and $z \in [0, 15]$. This ensures a sharp, non-filleted internal corner.
- **Motor Interface (R5)**: A clearance pocket is subtracted from the geometry to accommodate the motor body. To prevent "chamfered clearance" artifacts, this volume is modeled as a perfectly rectangular cuboid with sharp edges in the region $-21.5 \le x \le 21.5$, $-48 \le y \le 0$, and $8.5 \le z \le 51.5$. This subtraction is performed as a final step after the union of the plates.

**Load Path**: The motor's reaction force is applied at the face plate ($y=0$), transferred through the $y \in [0, 4]$ thickness into the non-filleted corner junction, and distributed through the base plate into the table via two M5 mounting screws.

**Requirement Compliance**:
- R1: Created using a single boolean union of the Face Plate and Base Plate (incorporating the Corner Overlap), followed by subtractions for holes (ensuring R6 holes are subtracted from the combined solid) and the R5 clearance cuboid.
- R2: Face plate thickness is strictly $4\text{ mm}$ ($y=0$ to $y=4$), ensuring solid material remains around all bores.
- R3: Central bore $\varnothing 22.5\text{ mm}$ is centered at $(x=0, z=30)$ and passes through the face plate along the Y-axis.
- R4: Four motor holes $\varnothing 3.4\text{ mm}$ are located at $(\pm 15.5, 14.5)$ and $(\pm 15.5, 45.5)$ on the face plate (calculated as $30 \pm 15.5$).
- R5: A rectangular cuboid clearance volume is subtracted to ensure no material interferes with the NEMA 17 body in the specified $x, y, z$ range.
- R6: Two vertical base holes $\varnothing 5.5\text{ mm}$ are located at $(x, y) = (\pm 25, 25)$, extending from $z=0$ to $z=15$ (the full thickness of the Base Plate).
- R7: Envelope is constrained within $-35 \le x \le 35$ and $z_{max} \le 55\text{ mm}$; mass is optimized to stay under $60\text{ g}$ using PLA density.