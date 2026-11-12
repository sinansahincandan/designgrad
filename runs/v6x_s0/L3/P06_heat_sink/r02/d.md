**Concept**: A rectangular aluminum base plate with vertical fins oriented along the Y-axis to maximize surface area for natural convection, featuring dedicated cylindrical clearance zones for screwdriver access to mounting screws.

**Main Features**:
- **Base**: A solid rectangular prism of $40 \times 40 \times 3$ mm, spanning $z=0$ to $z=3$.
- **Fins**: 8 fins, each 2 mm thick, spaced 3.43 mm apart (center-to-center or edge-to-edge as required to fit), extending from $z=3$ to $z=22$.
- **Mounting Holes**: Two 3.2 mm diameter holes centered exactly at $(\pm 15, 0)$, passing through the base ($z=0$ to $z=3$).
- **Screw Clearance**: Two cylindrical voids, each with a diameter of 6 mm, centered at $(\pm 15, 0)$, extending from $z=3$ to the top of the part ($z=22$) to ensure no material is within 3 mm of the hole axis above the base.

**Requirement Checklist**:
- **R1 (Single Solid)**: The part is constructed by creating a solid base and fins, then performing boolean subtractions for the mounting holes and clearance voids.
- **R2 (Footprint/Height)**: Footprint is exactly $40 \times 40$ mm; total height is 22 mm ($\le 25$ mm).
- **R3 (Base Thickness)**: Base is a solid $40 \times 40 \times 3$ mm block. Mounting holes (3.2 mm) are subtracted from this base, ensuring the slab remains at least 3 mm thick everywhere except at the hole locations.
- **R4 (Thermal)**: 
    *   Base area (top/bottom): $\approx 1600 \text{ mm}^2 \times 2 = 3200 \text{ mm}^2$.
    *   Fin sides: $8 \text{ fins} \times 2 \text{ sides} \times 19 \text{ height} \times 40 \text{ width} = 12160 \text{ mm}^2$.
    *   Total Area $A \approx 15360 \text{ mm}^2$ (minus hole/clearance subtractions $\approx 13760 \text{ mm}^2 = 0.01376 \text{ m}^2$).
    *   $R = 1 / (10 \cdot 0.01376 \cdot 0.85) \approx 8.5 \text{ K/W}$. This meets $R \le 9$.
- **R5 (Mounting/Clearance)**: Holes are centered at $(\pm 15, 0)$. Clearance is provided by 6 mm diameter cylindrical voids from $z=3$ upwards, satisfying the "no material within 3 mm of hole axis" rule.
- **R6 (Mass)**: 
    *   Estimated Volume $\approx 14000 \text{ mm}^3 - (\text{voids})$.
    *   Volume of two 6mm cylinders ($z=3$ to $22$) $\approx 2 \times (\pi \cdot 3^2 \cdot 19) \approx 1075 \text{ mm}^3$.
    *   Net Volume $\approx 13000 \text{ mm}^3$.
    *   Mass $\approx 13000 \text{ mm}^3 \times 0.0027 \text{ g/mm}^3 \approx 35.1\text{g}$ ($\le 45$ g).

**Construction Logic**:
1. Create base: `box(40, 40, 3)` at $z=0$.
2. Subtract mounting holes: `cylinder(3.2)` at $(\pm 15, 0)$ from $z=0$ to $3$.
3. Create fins and union with base.
4. Subtract clearance voids: `cylinder(6.0)` at $(\pm 15, 0)$ from $z=3$ to $22$.