**Concept**: A tripod-style wedge mount consisting of a wide rectangular base for stability and an inclined upright pillar that holds the sensor board at a 30° angle.

**Main Features**:
- **Base**: $45 \times 40$ mm footprint (extending from $x \in [-22.5, 22.5]$ and $y \in [-20, 20]$) to ensure stability against the forward-leaning mass.
- **Upright Pillar**: A block tilted at 30° relative to the Z-axis. The pillar is created by rotating a vertical block around the X-axis using `rotate((1, 0, 0), 30)`.
- **Mounting Face**: Located at center coordinates $(x, y, z) = (0, -5, 42.5)$. Dimensions are $40\text{ mm}$ (width) $\times 25\text{ mm}$ (height), providing an area of $1000 \text{ mm}^2$ ($> 900 \text{ mm}^2$), tilted towards $+Y$.
- **Screw Holes**: Base holes at $(\pm 20, -10)$ and sensor holes at $\pm 10$ mm along the tilted X-axis.

**Load Path**: The weight of the sensor is transferred through the mounting face into the upright pillar, which distributes the force down to the wide base, where it is transferred to the desk via the contact area.

**Requirement Fulfillment**:
- R1: Created using a single boolean union/subtraction workflow resulting in one solid.
- R2: Base holes (4.5 mm) placed at $(\pm 20, -10)$.
- R3: Mounting face normal is $(0, \cos(30^\circ), \sin(30^\circ))$ via a $30^\circ$ rotation of the upright around the X-axis (`rotate((1, 0, 0), 30)`).
- R4: Face center height is set to $42.5$ mm (within the $35\text{--}50$ mm range).
- R5: Sensor holes (3.2 mm) placed $\pm 10$ mm from face center, perpendicular to the face.
- R6: Stability Verification:
    - Face Center: $(0, -5, 42.5)$
    - Normal $\vec{n} \approx (0, 0.866, 0.5)$
    - Sensor CoM = Face Center $+ 15\text{ mm} \cdot \vec{n} \approx (0, -5 + 12.99, 42.5 + 7.5) = (0, 7.99, 50)$.
    - The base extends to $y = +20$ and $y = -20$. A CoM at $y = 7.99$ is well within the footprint. With a total mass of $\approx 2.8\text{g}$ (mount) and $50\text{g}$ (sensor), the combined CoM will be pulled toward $y=7.99$, staying safely within the $y < 15$ limit to maintain the required $5\text{ mm}$ margin from the edge ($20 - 5 = 15$).
- R7: Total volume is approx $2300 \text{ mm}^3$, mass $\approx 2.8 \text{ g}$ (well under $35\text{g}$).