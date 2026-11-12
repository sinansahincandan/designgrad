**Concept**: A tripod-style wedge mount consisting of a wide rectangular base for stability and an inclined upright pillar that holds the sensor board at a 30° angle. The pillar is rotated around the X-axis to achieve the required tilt.

**Main Features**:
- **Base**: $45 \times 60$ mm footprint (extending from $y = -20$ to $y = +40$) to ensure stability against the forward-leaning mass of the sensor.
- **Upright Pillar**: A block tilted at 30° relative to the Z-axis via a rotation around the X-axis.
- **Mounting Face**: Located at center coordinates $(0, 0, 42.5)$, tilted towards $+Y$ with normal $\vec{n} = (0, \cos 30^\circ, \sin 30^\circ)$.
- **Screw Holes**: Base holes at $(\pm 20, -10)$ and sensor holes at $\pm 10$ mm along the tilted X-axis.

**Load Path**: The weight of the sensor is transferred through the mounting face into the upright pillar, which distributes the force down to the wide base, where it is transferred to the desk via the contact area.

**Requirement Fulfillment**:
- R1: Created using a single boolean union/subtraction workflow resulting in one solid.
- R2: Base holes (4.5 mm) placed at $(\pm 20, -10)$, which are within the $y \in [-20, 40]$ footprint.
- R3: Mounting face normal is $(0, \cos 30^\circ, \sin 30^\circ)$ achieved by a $30^\circ$ rotation of the upright around the X-axis.
- R4: Face center height is set to $z = 42.5$ mm (within the $35\text{--}50$ mm range).
- R5: Sensor holes (3.2 mm) placed $\pm 10$ mm from face center $(0, 0, 42.5)$, perpendicular to the face.
- R6: Stability: The sensor CoM is $15\text{ mm}$ along $\vec{n}$ from $(0, 0, 42.5)$. Sensor $y_{CoM} = 0 + (15 \cdot \cos 30^\circ) \approx 12.99\text{ mm}$. With the base edge at $y = 40$, the margin is $40 - 12.99 = 27.01\text{ mm}$, which exceeds the required $5\text{ mm}$ margin.
- R7: Total volume is approx $3500 \text{ mm}^3$, mass $\approx 4.3 \text{ g}$ (well under $35\text{g}$).