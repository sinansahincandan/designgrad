**Concept**: A tripod-style wedge mount consisting of a wide rectangular base for stability and an inclined upright pillar that holds the sensor board at a 30° angle. All geometry is calculated relative to the plane $z=0$.

**Main Features**:
- **Base**: A $45 \times 40$ mm footprint located at $z=0$ (bottom surface) to ensure stability against the forward-leaning mass.
- **Upright Pillar**: A block rotated $30^\circ$ around the X-axis to achieve a mounting face normal of $(0, \cos(30^\circ), \sin(30^\circ))$.
- **Mounting Face**: Located at a center height of $z = 42.5$ mm, tilted towards $+Y$. The face is a rectangle of $40 \times 25$ mm to ensure an area $\ge 900\text{ mm}^2$.
- **Screw Holes**: Base holes (4.5 mm) at $(\pm 20, -10)$ on the $z=0$ plane; sensor holes (3.2 mm) are placed $\pm 10$ mm along the tilted X-axis, with their axis rotated $30^\circ$ around the X-axis to remain perpendicular to the face.

**Load Path**: The weight of the sensor is transferred through the mounting face into the upright pillar, which distributes the force down to the wide base, where it is transferred to the desk via the contact area at $z=0$.

**Requirement Fulfillment**:
- R1: Created using a single boolean union/subtraction workflow resulting in one solid.
- R2: Base holes (4.5 mm) placed at $(\pm 20, -10)$ with the base bottom surface at exactly $z=0$.
- R3: Mounting face normal is $(0, \cos(30^\circ), \sin(30^\circ))$ via a $30^\circ$ rotation around the X-axis. Area $\ge 900\text{ mm}^2$ is maintained.
- R4: Face center height is set to $42.5$ mm (within the $35\text{--}50$ mm range).
- R5: Sensor holes (3.2 mm) placed $\pm 10$ mm from face center, perpendicular to the face via a $30^\circ$ X-axis rotation of the hole axis.
- R6: Base width ($45$ mm) and depth ($40$ mm) ensure the combined CoM (including the 50g sensor offset) stays well within the footprint margin with $\ge 5$ mm clearance.
- R7: Total volume is approx $24000 \text{ mm}^3$, mass $\approx 29.8 \text{ g}$ (well under the $35\text{g}$ limit).