**Concept**: An L-shaped bracket designed to mount a NEMA 17 stepper motor. It consists of a vertical face plate (on the +Y side) and a horizontal base plate (resting on the table at z=0), joined into a single continuous solid.

**Main Features**:
- **Face Plate**: A solid block defined by $x \in [-35, 35]$, $y \in [0, 4]$, and $z \in [0, 55]$. It provides the mounting surface for the motor.
- **Base Plate**: A horizontal plate resting on the table ($z=0$) with a footprint of $x \in [-35, 35]$ and $y \in [0, 50]$, designed with a specific thickness to keep total mass under 60g.
- **Motor Interface**: The motor's shaft axis is at $(x=0, z=30)$. A central bore passes through the face plate along the Y-axis.
- **Clearance Zone (R5)**: To prevent interference with the motor body ($42.3 \times 48$ mm), a rectangular volume defined by $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$ is subtracted from the bracket geometry.
- **Load Path**: Motor torque and axial loads are transferred through the face plate into the base plate, then secured to the table via two vertical M5 screws.

**Requirements Fulfillment**:
- **R1 (Single Solid)**: The part is constructed by performing a `union()` of the Face Plate and Base Plate, followed by the subtraction of all holes and the motor clearance volume.
- **R2 (Face Plate Thickness)**: The face plate is defined from $y=0$ to $y=4$, ensuring a 4mm thickness with solid material surrounding the central bore.
- **R3 (Central Bore)**: A $\varnothing 22.5$ mm through-hole is drilled along the Y-axis at $(x=0, z=30)$.
- **R4 (Motor Holes)**: Four $\varnothing 3.4$ mm holes are drilled through the face plate along the Y-axis at coordinates $(x, z) = (\pm 15.5, 30 \pm 15.5)$.
- **R5 (Motor Clearance)**: The forbidden zone $x \in [-21.5, 21.5], y \in [-48, 0], z \in [8.5, 51.5]$ is explicitly subtracted from the solid.
- **R6 (Base Holes)**: Two vertical $\varnothing 5.5$ mm holes are drilled along the Z-axis through the base plate at $(x, y) = (\pm 25, 25)$.
- **R7 (Envelope & Mass)**: 
    - The geometry is constrained to $x \in [-35, 35]$ and $z_{max} = 55$.
    - To ensure mass $\le 60$ g using PLA ($\rho = 1.24 \text{ g/cm}^3$), the total volume is kept below $48,387 \text{ mm}^3$ by optimizing the base plate thickness and removing unnecessary material.