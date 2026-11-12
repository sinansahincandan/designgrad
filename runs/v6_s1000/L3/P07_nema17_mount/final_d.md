**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the NEMA 17 motor and a horizontal base plate to secure it to the table at $z=0$.

**Main Features**:
- **Face Plate**: A vertical component occupying $y \in [0, 4]$. It extends from $z=0$ to $z=55$ to satisfy R7. It contains the central shaft bore and four M3 mounting holes.
- **Base Plate**: A horizontal component sitting on the table ($z=0$) that starts at the face plate boundary ($y=4$) and extends into the $+Y$ direction (e.g., $y \in [4, 50]$). This prevents interference with the motor body in the $y < 0$ region.
- **Motor Clearance (R5)**: To ensure zero interference with the motor body, a large void is maintained in the region defined by $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$.
- **Load Path**: Motor torque and axial loads are transferred through the face plate into the base plate, then via two vertical M5 screws through the base plate into the table.

**Requirements Fulfillment**:
- **R1 (Single Solid)**: Created as a single continuous solid using boolean union of the L-shape geometry minus the specified holes and clearance pocket.
- **R2 (Face Plate Thickness & Integrity)**: The face plate is defined with a thickness of 4mm ($y=0$ to $y=4$). To ensure sufficient material around the central bore, the face plate height is set from $z=0$ to $z=55$. This ensures that even at the top edge ($z=55$), there is significant material remaining above the motor clearance zone.
- **R3 (Central Bore)**: A $\varnothing 22.5$ mm hole (implemented as a subtractive cylinder with radius $11.25$ mm) is drilled through the face plate along the Y-axis, centered at $(x=0, z=30)$.
- **R4 (Motor Holes)**: Four $\varnothing 3.4$ mm holes (radius $1.7$ mm) are implemented as subtractive cylinders through the face plate along the Y-axis at $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- **R5 (Motor Clearance)**: A subtraction operation ensures no geometry exists within $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$.
- **R6 (Base Holes)**: Two $\varnothing 5.5$ mm holes are implemented as subtractive cylinders drilled vertically along the Z-axis starting from $z=0$ at $(x, y) = (\pm 25, 25)$.
- **R7 (Envelope & Mass)**: 
    - The envelope is constrained to $x \in [-35, 35]$ and $z_{max} = 55$ mm.
    - To meet the mass limit ($\le 60$ g) using PLA ($\rho = 1.24 \text{ g/cm}^3$), the total volume $V$ must be $\le 48.38 \text{ cm}^3$. This is achieved by optimizing base plate thickness and applying weight-reduction cutouts in the base area (outside the R5 clearance zone and R6 hole zones).