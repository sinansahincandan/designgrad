**Concept**: A tapered I-beam profile drone arm designed to maximize the second moment of area ($I$) while minimizing mass. The cross-section at $x=20$ is an I-shape to satisfy strength and stiffness requirements.

**Main Features**:
- **Profile**: Tapered I-beam with a base width of 30mm at the frame and narrowing towards the motor.
- **Cross-Sectional Geometry (at x=20)**:
    - Height ($h$): $14\text{ mm}$
    - Flange width ($b_f$): $30\text{ mm}$
    - Flange thickness ($t_f$): $2\text{ mm}$
    - Web thickness ($t_w$): $1.5\text{ mm}$
- **Frame Attachment**: Two $\varnothing 3.2\text{ mm}$ holes at $(6, \pm 6)$.
- **Motor Mount**: Four $\varnothing 3.2\text{ mm}$ holes at $(120 \pm 8, \pm 9.5)$ and a central $\varnothing 6\text{ mm}$ shaft hole.
- **Dimensions**: Length $130\text{ mm}$, height $14\text{ mm}$, width varies from $30\text{ mm}$ to $20\text{ mm}$.

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created using boolean operations on a single continuous extrusion/lofting logic.
- R2: Envelope is $130 \times 30 \times 14\text{ mm}$, within limits.
- R3: Holes placed at $(6, \pm 6)$ with diameter $3.2\text{ mm}$.
- R4: Motor holes at $(120 \pm 8, \pm 9.5)$ and shaft hole at $(120, 0)$.
- R5: At $x=20$, Moment $M = 12\text{ N} \times (120-20) = 1200\text{ Nmm}$. 
    - Using defined geometry: $I = \frac{30 \cdot 14^3}{12} - \frac{(30 - 1.5) \cdot (14 - 2 \cdot 2)^3}{12} = 7140 - 3088.75 = 4051.25\text{ mm}^4$.
    - Section Modulus $Z = I / (h/2) = 4051.25 / 7 = 578.75\text{ mm}^3$.
    - $\sigma = M/Z = 1200 / 578.75 \approx 2.07\text{ MPa}$, which is $< 30\text{ MPa}$.
- R6: At $x=20$, the I-beam section provides $I \approx 4051\text{ mm}^4$, which is $\gg 1.0\text{ mm}^4$.
- R7: Volume calculation based on average cross-section area ($\approx 115\text{ mm}^2$) over $130\text{ mm}$ length $\approx 15\text{ cm}^3$. Mass $\approx 15 \times 1.24 = 18.6\text{ g} < 20\text{ g}$.