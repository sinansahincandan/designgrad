**Concept**: An L-shaped bracket consisting of a vertical face plate to mount the NEMA 17 motor and a horizontal base plate to secure it to the table at $z=0$. The design uses a "pocketed" approach, subtracting material from the base plate to minimize mass while maintaining structural integrity around mounting points.

**Geometric Parameters Table**:
| Feature | Parameter | Value / Coordinates | Requirement Mapping |
| :--- | :--- | :--- | :--- |
| **Face Plate** | Dimensions ($x, y, z$) | $x \in [-35, 35], y \in [0, 4], z \in [0, 55]$ | R2, R7 |
| **Base Plate** | Dimensions ($x, y, z$) | $x \in [-35, 35], y \in [4, 50], z \in [0, 4]$ | R1, R6, R7 |
| **Central Bore** | Diameter, Center $(x, z)$ | $\varnothing 22.5$ mm @ $(0, 30)$ | R3 |
| **Motor Holes** | Diameter, Centers $(x, z)$ | $\varnothing 3.4$ mm @ $(\pm 15.5, 30 \pm 15.5)$ | R4 |
| **Table Holes** | Diameter, Centers $(x, y)$ | $\varnothing 5.5$ mm @ $(\pm 25, 25)$ | R6 |
| **Clearance Vol** | Prism ($x, y, z$) | $x \in [-21.5, 21.5], y \in [-48, 0], z \in [8.5, 51.5]$ | R5 |

**Main Features**:
- **Face Plate**: 4mm thick vertical wall providing the mounting surface for the motor.
- **Base Plate**: A horizontal plate extending from $y=4$ to $y=50$, resting on the table at $z=0$. It is 4mm thick ($z \in [0, 4]$).
- **Motor Interface**: A precise subtraction of the clearance volume ensures the motor body (42.3mm square) and shaft axis do not collide with the bracket.
- **Fasteners**: Four M3 holes for the NEMA 17 face and two M5 holes for table mounting.

**Construction Sequence (CadQuery Logic)**:
1. **Step 1 (Base Solid)**: Create a primary block for the Face Plate ($x \in [-35, 35], y \in [0, 4], z \in [0, 55]$).
2. **Step 2 (Union)**: Create and `union` a second block for the Base Plate ($x \in [-35, 35], y \in [4, 50], z \in [0, 4]$) to ensure a single continuous solid (R1).
3. **Step 3 (Subtractions)**:
    - `cut` the central bore (R3) through the face plate along the Y-axis.
    - `cut` four motor screw holes (R4) through the face plate along the Y-axis.
    - `cut` the motor clearance volume (R5) using a rectangular prism subtraction.
    - `cut` two vertical table mounting holes (R6) through the base plate along the Z-axis.
4. **Step 4 (Optimization)**: `cut` additional pockets from the base plate (e.g., $y \in [10, 45], z \in [4, 4]$ is not possible, so rather $z \in [4, 4]$ is top; pocketing occurs in the $z$ dimension or by reducing width) to ensure mass $\le 60$g.

**Mass Calculation Logic**:
- **Total Volume** $\approx V_{face\_plate} + V_{base\_plate} - V_{holes} - V_{clearance} - V_{pockets}$.
- **Target Mass**: $M = \text{Volume} \times 1.24 \text{ g/cm}^3$.
- To ensure $M < 60\text{g}$, the pocketing strategy involves subtracting material from the base plate in regions not required for the R6 screw holes or structural connection to the face plate.

**Load Path**: Motor torque and axial thrust are transferred through the face plate to the base plate, which distributes the load into the table via the two M5 screw locations.

**Requirement Compliance**:
- **R1**: Single solid via `union` of face and base blocks.
- **R2**: Face plate thickness is 4mm ($y \in [0, 4]$).
- **R3**: Central bore $\varnothing 22.5$ mm at $(0, 30)$.
- **R4**: Four $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$.
- **R5**: Clearance volume $x: [-21.5, 21.5], y: [-48, 0], z: [8.5, 51.5]$ is subtracted.
- **R6**: Base plate includes two $\varnothing 5.5$ mm holes at $(\pm 25, 25)$.
- **R7**: Envelope $x \in [-35, 35]$, $z_{max} = 55$, mass optimized via pocketing to $< 60\text{g}$.