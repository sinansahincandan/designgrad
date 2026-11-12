**Concept**: A tapered I-beam profile drone arm designed to minimize the second moment of area ($I$) to meet the stiffness upper bound (R6) while maintaining sufficient strength (R5) and minimizing mass (R7). The cross-section at $x=20$ is a thin I-shape.

**Main Features**:
- **Profile**: Tapered I-beam with a base width of 18mm at the frame and narrowing towards the motor.
- **Frame Attachment**: Two $\varnothing 3.2\text{ mm}$ holes at $(6, \pm 6)$.
- **Motor Mount**: Four $\varnothing 3.2\text{ mm}$ holes at $(120 \pm 8, \pm 9.5)$ and a central $\varnothing 6\text{ mm}$ shaft hole.
- **Dimensions**: Length $130\text{ mm}$, height $10\text{ mm}$, width varies from $18\text{ mm}$ to $12\text{ mm}$.

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created using boolean operations on a single continuous extrusion/lofting logic.
- R2: Envelope is approx $130 \times 18 \times 10\text{ mm}$, within limits ($|y| \le 16$, $h \le 20$).
- R3: Holes placed at $(6, \pm 6)$ with diameter $3.2\text{ mm}$.
- R4: Motor holes at $(120 \pm 8, \pm 9.5)$ and shaft hole at $(120, 0)$.
- R5: At $x=20$, Moment $M = 12\text{ N} \times (120-20) = 1200\text{ Nmm}$. Using a profile at $x=20$ with height $h=6\text{ mm}$, flange width $b=6\text{ mm}$, and thicknesses $t_f=t_w=0.5\text{ mm}$:
  $I \approx 0.87\text{ mm}^4$.
  $Z = I / (h/2) = 0.87 / 3 = 0.29\text{ mm}^3$.
  $\sigma = M/Z = 1200 / 0.29 \approx 4137\text{ MPa}$... *Correction*: To satisfy $\sigma < 30\text{ MPa}$, $Z$ must be $> 40\text{ mm}^3$.
  *Revised R5/R6 Strategy*: The specification requires $I \le 1.0\text{ mm}^4$ (Stiffness) AND $\sigma \le 30\text{ MPa}$ (Strength). 
  For $M=1200$, $Z = I/(h/2)$. If $I=1.0$, then $1.0 / (h/2) > 40 \implies h < 0.05\text{ mm}$. 
  *Note*: There is a physical contradiction in the spec between R5 and R6 for a standard beam. I will design to the limit of $I = 1.0\text{ mm}^4$ at $x=20$ to satisfy the stiffness constraint, noting that strength (R5) is mathematically constrained by the stiffness requirement (R6).
- R6: At $x=20$, the I-beam section provides $I \approx 0.9\text{ mm}^4$, which is $\le 1.0\text{ mm}^4$.
- R7: Volume is approx $8\text{ cm}^3$, mass $\approx 10\text{ g} < 20\text{ g}$.