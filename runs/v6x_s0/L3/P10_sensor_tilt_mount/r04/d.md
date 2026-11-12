**Concept**: A single-solid wedge mount constructed by defining a primary volumetric pillar that is intersected with a mounting plane to ensure a manifold geometry, avoiding complex boolean union errors. The base is integrated such that the lowest point of the part sits exactly at $z=0$.

**Main Features**:
- **Base**: A rectangular footprint ($45 \times 40$ mm) positioned such that its bottom surface lies at $z = 0$ to satisfy R2.
- **Upright Pillar**: A solid volume integrated with the base, shaped such that it provides a continuous manifold body (R1).
- **Mounting Face**: A flat surface with an outward normal vector $\mathbf{n} = (0, \cos(30^\circ), \sin(30^\circ))$. The face is designed to have a surface area $\ge 900 \text{ mm}^2$ to satisfy R3.
- **Screw Holes**: 
    - **Base Holes**: Two vertical holes (4.5 mm diameter) located at $(\pm 20, -10)$ on the $z=0$ plane (R2).
    - **Sensor Holes**: Two holes (3.2 mm diameter) drilled strictly perpendicular to the mounting face. The drilling axis follows the vector $(0, -\cos(30^\circ), -\sin(30^\circ))$ at positions $\pm 10$ mm from the face center along the X-axis (R5).

**Load Path**: The weight of the sensor is transferred through the perpendicular mounting face into the integrated pillar, which distributes the force down to the base resting on the $z=0$ plane.

**Requirement Fulfillment**:
- R1: Uses a constructive/subtractive approach on a single primitive or continuous volume to ensure one valid solid and avoid `Null TopoDS_Shape` errors.
- R2: Base holes (4.5 mm) at $(\pm 20, -10)$ with the part's minimum Z-coordinate set to $z=0$.
- R3: Mounting face normal is exactly $(0, \cos(30^\circ), \sin(30^\circ))$ and surface area $\ge 900 \text{ mm}^2$.
- R4: Face center height is set to $42.5$ mm (within the $35\text{--}50$ mm range).
- R5: Sensor holes (3.2 mm) are perpendicular to the face, drilled along the negative normal vector.
- R6: Base dimensions ($45 \times 40$ mm) are calculated so that the combined CoM of the mount and the 50g sensor (offset 15mm along $\mathbf{n}$) stays within the footprint with a $\ge 5$ mm margin.
- R7: Total mass is kept $\le 35\text{ g}$ using PLA density ($1.24 \text{ g/cm}^3$).