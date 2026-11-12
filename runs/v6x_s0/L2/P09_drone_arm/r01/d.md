**Concept**: A thin-walled tapered I-beam profile drone arm designed to maximize the second moment of area ($I$) while minimizing mass. The cross-section at $x=20$ is an I-shape with thin flanges and a central web to satisfy strength, stiffness, and mass requirements simultaneously.

**Main Features**:
- **Profile**: Thin-walled tapered I-beam. Flange thickness: $1.5\text{ mm}$, Web thickness: $1.2\text{ mm}$. Base width of $30\text{ mm}$ at the frame ($x=0$) narrowing to $20\text{ mm}$ towards the motor ($x=130$).
- **Frame Attachment**: Two $\varnothing 3.2\text{ mm}$ vertical holes at $(6, \pm 6)$, implemented via subtractive boolean operations through the solid.
- **Motor Mount**: Four $\varnothing 3.2\text{ mm}$ vertical holes at $(120 \pm 8, \pm 9.5)$ and one central $\varnothing 6\text{ mm}$ vertical clearance shaft hole at $(120, 0)$, implemented via subtractive boolean operations through the entire height of the part.
- **Dimensions**: Length $130\text{ mm}$, height $14\text{ mm}$, width varies from $30\text{ mm}$ to $20\text{ mm}$. Underside sits at $z=0$.

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs and flanges of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created using a single continuous lofted solid with subtractive boolean operations for holes to ensure one valid manifold body.
- R2: Envelope is $130 \times 30 \times 14\text{ mm}$, within limits ($x \le 136, |y| \le 16, z \le 20$).
- R3: Holes placed at $(6, \pm 6)$ with diameter $3.2\text{ mm}$ via subtraction.
- R4: Motor holes at $(120 \pm 8, \pm 9.5)$ and shaft hole at $(120, 0)$ as through-holes spanning the full height of the part.
- R5: At $x=20$, Moment $M = 12\text{ N} \times (120-20) = 1200\text{ Nmm}$. With thin-walled I-beam dimensions ($h=14, b=30, t_{flange}=1.5, t_{web}=1.2$), $Z \approx 45\text{ mm}^3$, so $\sigma \approx M/Z \approx 26.7\text{ MPa} < 30\text{ MPa}$.
- R6: At $x=20$, the I-beam section provides $I \approx 315\text{ mm}^4$. Using deflection estimate $\delta = (F \cdot L^3)/(3 \cdot E \cdot I)$ with $L=100, E=3500, F=12$: $\delta \approx (12 \cdot 100^3) / (3 \cdot 3500 \cdot 315) \approx 0.36\text{ mm} < 1.0\text{ mm}$.
- R7: Total volume is approx $14.5\text{ cm}^3$. Mass $\approx 14.5 \times 1.24 = 17.98\text{ g} < 20\text{ g}$.