**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the NEMA 17 motor and a horizontal base plate to secure it to the table at $z=0$.

**Main Features**:
- **Face Plate**: A vertical component occupying $y \in [0, 4]$. It contains the central shaft bore and four M3 mounting holes.
- **Base Plate**: A horizontal component sitting on the table ($z=0$) that extends into the $+Y$ direction (e.g., $y \in [0, 50]$). It provides the footprint for stability and includes two vertical mounting holes.
- **Motor Clearance (R5)**: To ensure zero interference with the motor body, a large void is maintained in the region defined by $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$.
- **Load Path**: Motor torque and axial loads are transferred through the face plate into the base plate, then via two vertical M5 screws through the base plate into the table.

**Requirements Fulfillment**:
- **R1 (Single Solid)**: Created as a single continuous solid using boolean union of the L-shape geometry minus the specified holes and clearance pocket.
- **R2 (Face Plate Thickness)**: The face plate is defined with a thickness of 4mm ($y=0$ to $y=4$), ensuring sufficient material remains around the central bore.
- **R3 (Central Bore)**: A $\varnothing 22.5$ mm hole is drilled through the face plate along the Y-axis, centered at $(x=0, z=30)$.
- **R4 (Motor Holes)**: Four $\varnothing 3.4$ mm holes are drilled through the face plate along the Y-axis at $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- **R5 (Motor Clearance)**: A subtraction operation ensures no geometry exists within $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$.
- **R6 (Base Holes)**: Two $\varnothing 5.5$ mm holes are drilled vertically along the Z-axis at $(x, y) = (\pm 25, 25)$.
- **R7 (Envelope & Mass)**: 
    - The envelope is constrained to $x \in [-35, 35]$ and $z_{max} \le 55$.
    - To meet the mass limit ($\le 60$ g), the base plate thickness is optimized/reduced, and weight-reduction cutouts are applied in the base area (outside the R5 clearance zone and R6 hole zones) to ensure total volume $V < 48.38 \text{ cm}^3$.