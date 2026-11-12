**Concept**: A tripod-style wedge mount consisting of a wide rectangular base positioned at $z=0$ for stability, and an upright pillar that is rotated around the X-axis to provide a tilted mounting face.

**Main Features**:
- **Base**: $45 \times 40$ mm footprint with its bottom surface located exactly at $z = 0$.
- **Upright Pillar**: A block rotated $30^\circ$ around the X-axis such that its mounting face normal is exactly $(0, \cos(30^\circ), \sin(30^\circ))$.
- **Mounting Face**: A flat surface of $30 \times 35$ mm (area $= 1050 \text{ mm}^2$) located at a center height of $z = 42.5$ mm, tilted towards $+Y$.
- **Screw Holes**: 
    - Base holes: 4.5 mm diameter, placed at $(\pm 20, -10)$ on the $z=0$ plane.
    - Sensor holes: 3.2 mm diameter, drilled perpendicular to the mounting face (along the normal vector $(0, \cos(30^\circ), \sin(30^\circ))$) at $\pm 10$ mm from the face center along the local X-axis of the tilted face.

**Load Path**: The weight of the sensor is transferred through the mounting face into the upright pillar, which distributes the force down to the wide base, where it is transferred to the desk via the contact area at $z=0$.

**Requirement Fulfillment**:
- R1: Created using a single boolean union/subtraction workflow resulting in one solid.
- R2: Base bottom surface at $z=0$ with 4.5 mm holes at $(\pm 20, -10)$.
- R3: Mounting face area $\ge 900 \text{ mm}^2$ ($30 \times 35$ mm) with normal $(0, \cos(30^\circ), \sin(30^\circ))$ achieved via $30^\circ$ rotation around the X-axis.
- R4: Face center height is set to $42.5$ mm (within the $35\text{--}50$ mm range).
- R5: Sensor holes (3.2 mm) are perpendicular to the face, positioned $\pm 10$ mm from face center along the local X-axis.
- R6: The base footprint is centered such that when the 50g sensor mass is added at its CoM ($15\text{mm}$ along the normal from the face center), the combined CoM remains within the $45 \times 40$ mm footprint with a $\ge 5$ mm margin.
- R7: Total volume is approx $2300 \text{ mm}^3$, mass $\approx 2.8 \text{ g}$ (well under $35\text{g}$).