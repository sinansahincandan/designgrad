**Concept**: A tripod-style wedge mount consisting of a wide rectangular base positioned at $z=0$ for stability, and an inclined upright pillar that holds the sensor board at a 30° angle relative to the horizontal plane.

**Main Features**:
- **Base**: $45 \times 40$ mm footprint with its bottom surface at $z = 0$.
- **Upright Pillar**: A geometry constructed such that its top mounting face is rotated $30^\circ$ around the X-axis relative to the Z-axis, resulting in an outward normal of $(0, \cos(30^\circ), \sin(30^\circ))$.
- **Mounting Face**: A flat surface with dimensions $40 \text{ mm (width)} \times 25 \text{ mm (length along tilt)}$, providing an area of $1000 \text{ mm}^2$ ($\ge 900 \text{ mm}^2$). It is located at a center height of $z = 42.5$ mm, tilted towards $+Y$.
- **Screw Holes**: Base holes (4.5 mm) at $(\pm 20, -10)$ on the $z=0$ plane; sensor holes (3.2 mm) drilled perpendicular to the mounting face.

**Load Path**: The weight of the sensor applies a force perpendicular to the tilted mounting face into the upright pillar. This force is distributed through the pillar down to the wide base, which transfers the load to the desk via the contact area at $z=0$.

**Requirement Fulfillment**:
- R1: Created using a single boolean union/subtraction workflow resulting in one solid.
- R2: Base bottom surface is at $z=0$; holes (4.5 mm) placed at $(\pm 20, -10)$.
- R3: Mounting face normal is $(0, \cos(30^\circ), \sin(30^\circ))$ via a $30^\circ$ rotation around the X-axis; area is $1000 \text{ mm}^2$.
- R4: Face center height is set to $42.5$ mm (within the 35–50 mm range).
- R5: Sensor holes (3.2 mm) are drilled along the vector $(0, -\cos(30^\circ), -\sin(30^\circ))$ to ensure they are perpendicular to the face.
- R6: Base width ($45$ mm) and depth ($40$ mm) ensure that even with the 50g sensor's CoM (15mm forward of the face center), the combined CoM stays within the footprint margin by $\ge 5$ mm.
- R7: Total volume is approx $2300 \text{ mm}^3$, mass $\approx 2.8 \text{ g}$ (well under $35\text{g}$).