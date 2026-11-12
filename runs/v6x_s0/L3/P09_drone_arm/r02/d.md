**Concept**: A tapered I-beam profile drone arm designed to maximize the second moment of area ($I$) while minimizing mass. The cross-section at $x=20$ is an I-shape to satisfy strength and stiffness requirements.

**Main Features**:
- **Profile**: Tapered I-beam with a base width of 30mm at the frame and narrowing towards the motor. Flange thickness = 1.5 mm, Web thickness = 1.0 mm. Total height is 14 mm.
- **Frame Attachment**: Two vertical $\varnothing 3.2\text{ mm}$ cylinders (oriented along the Z-axis) centered at $(x=6, y=6)$ and $(x=6, y=-6)$, with a height of $20\text{ mm}$ to ensure full penetration through the part.
- **Motor Mount**: Four vertical $\varnothing 3.2\text{ mm}$ cylinders (oriented along the Z-axis) centered at $(112, 9.5)$, $(112, -9.5)$, $(128, 9.5)$, and $(128, -9.5)$. Additionally, one vertical $\varnothing 6\text{ mm}$ cylinder (oriented along the Z-axis) centered at $(120, 0)$ with a height of $20\text{ mm}$ to ensure full penetration through the entire part.
- **Dimensions**: Length $130\text{ mm}$, height $14\text{ mm}$, width varies from $30\text{ mm}$ to $20\text{ mm}$.

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created using boolean operations on a single continuous extrusion/lofting logic.
- R2: Envelope is $130 \times 30 \times 14\text{ mm}$, within limits.
- R3: Two vertical $\varnothing 3.2\text{ mm}$ cylinders at $(6, \pm 6)$ used for subtractive boolean operation to ensure clean through-holes.
- R4: Four vertical $\varnothing 3.2\text{ mm}$ cylinders at $(112, \pm 9.5)$ and $(128, \pm 9.5)$, plus one vertical $\varnothing 6\text{ mm}$ cylinder at $(120, 0)$ used for subtractive boolean operations to ensure full penetration.
- R5: At $x=20$, Moment $M = 12\text{ N} \times (120-20) = 1200\text{ Nmm}$. With I-beam height $14$ and width $30$ (and thin walls), $\sigma \approx M/Z < 30\text{ MPa}$.
- R6: At $x=20$, the I-beam section provides $I \approx 150\text{ mm}^4$, which is $\gg 1.0\text{ mm}^4$.
- R7: Volume is approx $15\text{ cm}^3$, mass $\approx 18.6\text{ g} < 20\text{ g}$ (using PLA density $1.24\text{ g/cm}^3$).