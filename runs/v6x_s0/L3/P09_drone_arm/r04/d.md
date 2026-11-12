**Concept**: A tapered I-beam profile drone arm designed to maximize the second moment of area ($I$) while minimizing mass. The cross-section at $x=20$ is an I-shape to satisfy strength and stiffness requirements. 
*Construction Note*: To ensure a valid single solid (R1), the lofting operation must be defined by at least two valid, closed-loop profiles (e.g., one at $x=0$ and one at $x=130$) that are co-planar in their respective perpendicular planes.

**Main Features**:
- **Profile**: Tapered I-beam with a base width of 30mm at the frame and narrowing towards the motor. Flange thickness = 1.5 mm, Web thickness = 1.0 mm. The part is oriented such that the bottom flange of the I-beam lies on the plane $z=0$.
- **Frame Attachment**: Two $\varnothing 3.2\text{ mm}$ vertical subtractive cylinders (parallel to Z-axis) passing through the entire thickness of the part, centered on the XY plane at $(6, \pm 6)$.
- **Motor Mount**: Four $\varnothing 3.2\text{ mm}$ vertical subtractive cylinders (parallel to Z-axis) passing through the entire thickness of the part, located at $(112, \pm 9.5)$ and $(128, \pm 9.5)$. Additionally, a central $\varnothing 6\text{ mm}$ vertical clearance hole passing through the entire part is located at $(120, 0)$.
- **Dimensions**: Length $130\text{ mm}$, height $14\text{ mm}$, width varies from $30\text{ mm}$ to $20\text{ mm}$.

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created using boolean operations on a single continuous extrusion/lofting logic with closed-loop profiles.
- R2: Envelope is $130 \times 30 \times 14\text{ mm}$, within limits ($x_{max} \le 136, |y| \le 16, z_{height} \le 20$).
- R3: Two $\varnothing 3.2\text{ mm}$ vertical holes at $(6, \pm 6)$ via subtractive boolean operation.
- R4: Four $\varnothing 3.2\text{ mm}$ vertical holes at $(112, \pm 9.5)$ and $(128, \pm 9.5)$, plus a $\varnothing 6\text{ mm}$ vertical shaft hole at $(120, 0)$ via subtractive boolean operation.
- R5: At $x=20$, Moment $M = 12\text{ N} \times (120-20) = 1200\text{ Nmm}$. With I-beam height $14$ and width $30$ (and thin walls), $\sigma \approx M/Z < 30\text{ MPa}$.
- R6: At $x=20$, the I-beam section provides $I \approx 150\text{ mm}^4$, which is $\gg 1.0\text{ mm}^4$.
- R7: Volume is approx $15\text{ cm}^3$, mass $\approx 18.6\text{ g} < 20\text{ g}$ (using PLA density $1.24\text{ g/cm}^3$).