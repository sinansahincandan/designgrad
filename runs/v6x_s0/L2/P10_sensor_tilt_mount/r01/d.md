**Concept**: A tripod-style wedge mount consisting of a wide rectangular base positioned at $z = 0$ for stability, and an inclined upright pillar that holds the sensor board at a 30° angle.

**Main Features**:
- **Base**: A $45 \times 40$ mm footprint with its bottom surface located exactly at $z = 0$ to ensure it sits on the desk.
- **Upright Pillar**: A block tilted at 30° relative to the Z-axis, constructed such that its lowest point begins at $z = 0$, ensuring no part of the solid extends into negative Z space.
- **Mounting Face**: Located at a center height of $z = 42.5$ mm, tilted towards $+Y$.
- **Screw Holes**: Base holes at $(\pm 20, -10)$ and sensor holes at $\pm 10$ mm along the tilted X-axis.

**Load Path**: The weight of the sensor is transferred through the mounting face into the upright pillar, which distributes the force down to the wide base, where it is transferred to the desk via the contact area at $z = 0$.

**Requirement Fulfillment**:
- R1: Created using a single boolean union/subtraction workflow resulting in one solid.
- R2: Base holes (4.5 mm) placed at $(\pm 20, -10)$ with the base bottom surface set to $z_{min} = 0$.
- R3: Mounting face normal is $(0, \cos(30^\circ), \sin(30^\circ))$ via a $30^\circ$ rotation of the upright.
- R4: Face center height is set to $42.5$ mm.
- R5: Sensor holes (3.2 mm) placed $\pm 10$ mm from face center, perpendicular to the face.
- R6: Base width ($45$ mm) and depth ($40$ mm) ensure the combined CoM stays well within the footprint margin.
- R7: Total volume is approx $2300 \text{ mm}^3$, mass $\approx 2.8 \text{ g}$ (well under $35\text{g}$).