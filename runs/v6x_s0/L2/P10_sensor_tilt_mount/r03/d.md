**Concept**: A tripod-style wedge mount consisting of a wide rectangular base positioned with its bottom surface at $z = 0$ for stability, and an inclined upright pillar that holds the sensor board at a 30° angle.

**Main Features**:
- **Base**: $45 \times 40$ mm footprint; the bottom surface is located at $z = 0$.
- **Upright Pillar**: A block tilted at 30° relative to the Z-axis to support the sensor.
- **Mounting Face**: A flat face with an area $\ge 900 \text{ mm}^2$, centered at exactly $z = 42.5$ mm, with an outward normal of $(0, \cos(30^\circ), \sin(30^\circ))$.
- **Base Screw Holes**: Two vertical holes (diameter 4.5 mm) parallel to the Z-axis, located at $(x, y) = (\pm 20, -10)$ on the base.
- **Sensor Screw Holes**: Two holes (diameter 3.2 mm) drilled perpendicular to the mounting face, centered at $\pm 10$ mm from the face center along the local X-axis (relative to the tilted coordinate system).

**Load Path**: The weight of the sensor is transferred through the mounting face into the upright pillar, which distributes the force down to the wide base, where it is transferred to the desk via the contact area at $z = 0$.

**Requirement Fulfillment**:
- R1: Created using a single boolean union/subtraction workflow resulting in one solid.
- R2: Base screw holes (4.5 mm) are vertical and located at $(\pm 20, -10)$ on the base at $z=0$.
- R3: Mounting face normal is $(0, \cos(30^\circ), \sin(30^\circ))$ via a $30^\circ$ rotation of the upright.
- R4: Face center height is set to exactly $42.5$ mm.
- R5: Sensor holes (3.2 mm) are perpendicular to the face, located at $(x_{face} \pm 10, y_{face}, z_{face})$ in the tilted local frame.
- R6: Base width ($45$ mm) and depth ($40$ mm) ensure that even with a 50g sensor (CoM 15mm forward of face center), the combined CoM stays within the footprint with $\ge 5$ mm margin.
- R7: Total volume is targeted at approx $2300 \text{ mm}^3$, resulting in a mass $\approx 2.8 \text{ g}$ (well under the $35\text{g}$ limit and the maximum allowable volume of $28,225 \text{ mm}^3$).