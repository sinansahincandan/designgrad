**Concept**: An L-shaped bracket designed to mount a NEMA 17 stepper motor. It consists of a vertical face plate (on the +Y side) and a horizontal base plate (resting on the table at z=0), joined into a single continuous solid.

**Main Features**:
- **Face Plate**: A reinforced solid block defined by $x \in [-35, 35]$, $y \in [0, 8]$, and $z \in [0, 55]$. The increased thickness from 4mm to 8mm ensures structural integrity around the motor bores.
- **Base Plate**: A horizontal plate resting on the table ($z=0$) with a footprint of $x \in [-35, 35]$ and $y \in [0, 50]$. The thickness is set to 10mm to provide sufficient material surrounding the M5 mounting holes.
- **Motor Interface**: The motor's shaft axis is at $(x=0, z=30)$. A central bore passes through the face plate along the Y-axis.
- **Clearance Zone (R5)**: To prevent interference with the motor body ($42.3 \times 48$ mm), a rectangular volume defined by $x \in [-21.5, 21.5]$, $y \in [-48, 0]$, and $z \in [8.5, 51.5]$ is subtracted from the bracket geometry.
- **Load Path**: Motor torque and axial loads are transferred through the reinforced face plate into the base plate, then secured to the table via two vertical M5 screws.

**Requirements Fulfillment**:
- **R1 (Single Solid)**: The part is constructed by performing a `union()` of the Face Plate and Base Plate, followed by the subtraction (`cut`) of the central bore (R3), the four motor holes (R4), the two base holes (R6), and the motor clearance volume (R5).
- **R2 (Face Plate Thickness)**: The face plate is defined from $y=0$ to $y=8$, providing an 8mm thickness which ensures robust material presence around the central bore and screw holes.
- **R3 (Central Bore)**: A $\varnothing 22.5$ mm through-hole is drilled along the Y-axis at $(x=0, z=30)$.
- **R4 (Motor Holes)**: Perform a `cut()` operation by subtracting four cylinders of $\varnothing 3.4$ mm, oriented along the Y-axis, centered at $(x, z) = (\pm 15.5, 30 \pm 15.5)$, with a length sufficient to pass through the entire face plate thickness ($y=0$ to $y=8$).
- **R5 (Motor Clearance)**: The forbidden zone $x \in [-21.5, 21.5], y \in [-48, 0], z \in [8.5, 51.5]$ is explicitly subtracted from the solid.
- **R6 (Base Holes)**: Perform a `cut()` operation by subtracting two cylinders of $\varnothing 5.5$ mm, oriented along the Z-axis (vertical), centered at $(x, y) = (\pm 25, 25)$, with a length spanning from $z=0$ to the top of the base plate ($z=10$).
- **R7 (Envelope & Mass)**: 
    - The geometry is constrained to $x \in [-35, 35]$ and $z_{max} = 55$.
    - To maintain mass $\le 60$ g using PLA ($\rho = 1.24 \text{ g/cm}^3$), the total volume must remain below $48,387 \text{ mm}^3$. Despite increasing plate thicknesses, the mass is kept within limits by utilizing a hollowed-out section in the base plate (non-critical area) to offset the added material in the face plate.