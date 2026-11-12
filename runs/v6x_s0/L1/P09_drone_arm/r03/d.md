**Concept**: A tapered I-beam profile drone arm designed to maximize the second moment of area ($I$) while minimizing mass. The cross-section at $x=20$ is an I-shape to satisfy strength and stiffness requirements within the envelope constraints.

**Main Features**:
- **Profile**: Tapered I-beam with a base width of 30mm at the frame and narrowing towards the motor.
- **Cross-Section Geometry (at x=20)**:
    - **Flange width ($b$):** $30\text{ mm}$
    - **Flange thickness ($t_f$):** $1.5\text{ mm}$
    - **Web thickness ($t_w$):** $2.0\text{ mm}$
    - **Total height ($h$):** $14\text{ mm}$ (Top surface at $z=14$, bottom at $z=0$)
- **Frame Attachment**: Two $\varnothing 3.2\text{ mm}$ holes at $(6, \pm 6)$.
- **Motor Mount**: Four $\varnothing 3.2\text{ mm}$ holes at $(120 \pm 8, \pm 9.5)$ and a central $\varnothing 6\text{ mm}$ shaft hole through the entire part.
- **Dimensions**: Length $130\text{ mm}$, height $14\text{ mm}$, width varies from $30\text{ mm}$ to $20\text{ mm}$.

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created using boolean operations on a single continuous extrusion/lofting logic.
- R2: Envelope is $130 \times 30 \times 14\text{ mm}$, within limits ($x_{max} \le 136, |y| \le 16, z_{max} \le 20$). Underside at $z=0$.
- R3: Holes placed at $(6, \pm 6)$ with diameter $3.2\text{ mm}$.
- R4: Motor holes at $(120 \pm 8, \pm 9.5)$ and shaft hole at $(120, 0)$.
- R5: At $x=20$, Moment $M = 12\text{ N} \times (120-20) = 1200\text{ Nmm}$. 
  Calculated $I$ for the section: $I \approx \frac{30 \cdot 14^3}{12} - \frac{(30-2) \cdot (14-3)^3}{12} \approx 4802 - 2849 = 1953\text{ mm}^4$.
  $\sigma = \frac{M \cdot (h/2)}{I} = \frac{1200 \cdot 7}{1953} \approx 4.3\text{ MPa}$, which is $\le 30\text{ MPa}$.
- R6: At $x=20$, the I-beam section provides $I \approx 1953\text{ mm}^4$. While this exceeds the specification's literal requirement of $I \le 1.0\text{ mm}^4$ (which is physically contradictory to R5), it ensures structural integrity and follows the logical intent of a stiffness requirement ($I \ge 1.0$).
- R7: Volume is approx $13\text{ cm}^3$, mass $\approx 16\text{ g} < 20\text{ g}$ (using PLA density 1.24).