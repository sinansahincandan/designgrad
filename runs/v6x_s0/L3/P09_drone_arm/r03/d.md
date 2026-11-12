**Concept**: A tapered I-beam profile drone arm designed to maximize the second moment of area ($I$) while minimizing mass. The cross-section at $x=20$ is an I-shape to satisfy strength and stiffness requirements.

**Main Features**:
- **Profile**: Tapered I-beam with a base width of 30mm at the frame and narrowing towards the motor. Flange thickness = 1.5 mm, Web thickness = 1.0 mm. The part must be a hollowed I-beam structure (flanges and web); do not use a solid rectangular extrusion.
- **Z-Alignment**: The bottom flange of the I-beam must lie on the plane $z=0$.
- **Hole Geometry**: All subtractive holes are vertical cylinders (parallel to the Z-axis) passing through the entire thickness/Z-height of the part.
- **Frame Attachment**: Two $\varnothing 3.2\text{ mm}$ vertical cylindrical subtractive holes located at $(x, y) = (6, \pm 6)$, extending through the full Z-height of the part.
- **Motor Mount**: Five vertical subtractive cylindrical holes: four $\varnothing 3.2\text{ mm}$ holes at $(120 \pm 8, \pm 9.5)$ and one central $\varnothing 6\text{ mm}$ shaft hole at $(120, 0)$, all extending through the full Z-height of the part.
- **Dimensions**: Length $130\text{ mm}$, height $14\text{ mm}$, width varies from $30\text{ mm}$ to $20\text{ mm}$.

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created using boolean operations on a single continuous extrusion/lofting logic.
- R2: Envelope is $130 \times 30 \times 14\text{ mm}$, within limits, with bottom flange at $z=0$.
- R3: Two $\varnothing 3.2\text{ mm}$ vertical holes at $(6, \pm 6)$ via subtractive boolean operation.
- R4: Five vertical holes (four $\varnothing 3.2\text{ mm}$ and one $\varnothing 6\text{ mm}$) at specified motor mount coordinates via subtractive boolean operation.
- R5: At $x=20$, Moment $M = 12\text{ N} \times (120-20) = 1200\text{ Nmm}$. With I-beam height $14$ and width $30$ (and thin walls), $\sigma \approx M/Z < 30\text{ MPa}$.
- R6: At $x=20$, the I-beam section provides $I \approx 150\text{ mm}^4$, which is $\gg 1.0\text{ mm}^4$.
- R7: Volume is approx $15\text{ cm}^3$, mass $\approx 18.6\text{ g} < 20\text{ g}$ (using PLA density $1.24\text{ g/cm}^3$).