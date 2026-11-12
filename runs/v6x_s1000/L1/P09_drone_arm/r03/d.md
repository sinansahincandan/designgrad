**Concept**: A high-aspect-ratio "rib" style arm designed to satisfy the highly restrictive stiffness constraint ($I \le 1.0 \text{ mm}^4$) at $x=20$ while attempting to manage bending stress through vertical height. The profile is extremely thin to keep the second moment of area below the threshold specified in R6.

**Main Features**:
- **Base Section (x=0 to 30)**: A very thin, tall vertical rib. At $x=20$, dimensions are $w = 0.15$ mm and $h = 4.0$ mm. This ensures the second moment of area is kept low to meet R6.
- **Tapered Web (x=30 to 110)**: A transition from the thin base rib to a wider, more robust section at the motor mount.
- **Motor Mount (x=110 to 130)**: A widened flange section ($24 \times 12$ mm) to accommodate the four motor bolt holes and shaft clearance.
- **Load Path**: Vertical loads from the motor at $x=120$ are transferred through the mounting flanges into the central rib structure.

**Requirement Fulfillment**:
- R1: Created using a single `union` of primitives or a continuous sweep/lofting approach (implemented via boolean operations on a single body).
- R2: Envelope is approx $x \in [0, 130]$, $y \in [-12, 12]$, $z \in [0, 15]$.
- R3: Two $\varnothing 3.2$ mm holes at $(6, \pm 6)$ through the base.
- R4: Four $\varnothing 3.2$ mm holes at $(120 \pm 8, \pm 9.5)$ and one $\varnothing 6$ mm shaft hole at $(120, 0)$.
- R5: At $x=20$, $M = 12\text{N} \times (120-20)\text{mm} = 1200\text{ Nmm}$. With $h=4$ and $w=0.15$, $I = (0.15 \cdot 4^3)/12 = 0.8 \text{ mm}^4$. $\sigma = Mc/I = (1200 \cdot 2) / 0.8 = 3000\text{ MPa}$. *Note: As identified in the feedback, R5 ($\le 30$ MPa) and R6 ($I \le 1.0$) are mathematically contradictory for a single solid beam at this scale; the design prioritizes the explicit $I \le 1.0$ constraint to satisfy the stiffness requirement.*
- R6: At $x=20$, $I = 0.8 \text{ mm}^4$. This satisfies the requirement $I \le 1.0 \text{ mm}^4$.
- R7: Total volume is significantly reduced due to the thin rib, ensuring mass $\ll 20$ g.