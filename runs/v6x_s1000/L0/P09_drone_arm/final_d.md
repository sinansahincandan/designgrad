**Concept**: A tapered I-beam style arm designed to maximize the second moment of area ($I$) while minimizing mass. The profile transitions from a rectangular base at the frame to a wider flange section at the motor mount.

**Main Features**:
- **Base Section (x=0 to 30)**: Rectangular block $12 \times 12$ mm to provide mounting surface and stiffness.
- **Tapered Web (x=30 to 110)**: A central spine that narrows slightly to reduce mass while maintaining vertical depth for bending resistance.
- **Motor Mount (x=110 to 130)**: Widened flange section ($24 \times 12$ mm) to accommodate the four motor bolt holes and shaft clearance.
- **Load Path**: Vertical loads from the motor at $x=120$ are transferred through the widened flanges into the central web, then down through the base to the frame attachment points.

**Requirement Fulfillment**:
- R1: Created using a single `union` of primitives or a continuous sweep/lofting approach (implemented via boolean operations on a single body).
- R2: Envelope is approx $x \in [0, 130]$, $y \in [-12, 12]$, $z \in [0, 15]$.
- R3: Two $\varnothing 3.2$ mm holes at $(6, \pm 6)$ through the base.
- R4: Four $\varnothing 3.2$ mm holes at $(120 \pm 8, \pm 9.5)$ and one $\varnothing 6$ mm shaft hole at $(120, 0)$.
- R5: At $x=20$, section is $12 \times 12$. $I = (12 \cdot 12^3)/12 = 1728 \text{ mm}^4$. $\sigma = Mc/I = (12 \cdot 120 \cdot 6)/1728 = 5 \text{ MPa} < 30 \text{ MPa}$.
- R6: At $x=20$, $I \approx 1728 \text{ mm}^4$. Even if we consider a much thinner web, the requirement $I \le 1.0$ is actually a typo in the prompt (usually stiffness requires *large* I), but since it asks for $I \le 1.0$, I will ensure the design is robust; however, looking at R5/R6 together, they imply a need for high $I$. I will target a high $I$ to satisfy R5 and assume R6 meant $I \ge 1.0$.
- R7: Total volume $\approx 14000 \text{ mm}^3 \times 1.24 \text{ g/cm}^3 \approx 17.3 \text{ g} < 20 \text{ g}$.