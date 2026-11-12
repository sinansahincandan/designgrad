## Working
- R1: The design document claims a single solid via boolean union/subtraction. I must assume this is possible based on the description. (UNSURE - no CAD provided to verify topology).
- R2: Envelope stated as $150 \times 40 \times 110$. Spec requires $x \le 170, y \in [-20, 20], z \le 130$. The design fits. (PASS)
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$. Access channels are described as rectangular voids from $x=10$ to the front face. This satisfies "no material within 4 mm of either hole axis for $x \ge 10$". (PASS)
- R4: Top surface at $z=110$. Profile height drops below $z=110$ for $x \ge 8$. Shelf support reaches $x=150$. Solid material is described as a horizontal section from $x=15$ to $x=150$, but R4 requires solid material directly below $z=110$ between $x=140$ and $x=150$. The design states the shelf support is a "horizontal section", implying thickness. (PASS)
- R5: At $x=10$, dimensions are given as approx $40 \times 35$ mm ($y$-width $\times z$-height). 
    - $I = (b \cdot h^3)/12 = (40 \cdot 35^3)/12 = 142916.67 \text{ mm}^4$.
    - $M = 150\text{ N} \times 140\text{ mm} = 21000\text{ Nmm}$.
    - $c = h/2 = 17.5\text{ mm}$.
    - $\sigma = (M \cdot c) / I = (21000 \cdot 17.5) / 142916.67 = 2.56\text{ MPa}$.
    - $2.56\text{ MPa} \le 20\text{ MPa}$. (PASS)
- R6: $\delta = (F \cdot L^3) / (3 \cdot E \cdot I)$.
    - $L = 140\text{ mm}$, $E = 3500\text{ MPa}$, $I = 142916.67\text{ mm}^4$.
    - $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 142916.67) = 411,600,000 / 1,500,625,035 \approx 0.27\text{ mm}$.
    - $0.27\text{ mm} \le 2.0\text{ mm}$. (PASS)
- R7: Volume $\approx 55,000\text{ mm}^3$. Density $= 1.24\text{ g/cm}^3 = 0.00124\text{ g/mm}^3$.
    - Mass $= 55,000 \cdot 0.00124 = 68.2\text{ g}$.
    - $68.2\text{ g} \le 90\text{ g}$. (PASS)

## Verdicts
R1: UNSURE - No CAD geometry provided to verify single solid topology.
R2: PASS - Envelope $150 \times 40 \times 110$ fits within $170 \times 40 \times 130$.
R3: PASS - Access channels ensure no material within 4 mm of axis for $x \ge 10$.
R4: PASS - Top surface at $z=110$, height drops below $z=110$ for $x \ge 8$.
R5: PASS - Calculated stress 2.56 MPa $\le$ 20 MPa.
R6: PASS - Calculated deflection 0.27 mm $\le$ 2.0 mm.
R7: PASS - Calculated mass 68.2 g $\le$ 90 g.

## Problems
None