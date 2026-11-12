## Working
- R1: The design document claims a single solid via boolean union. Status: PASS (based on description).
- R2: Envelope claimed as $150 \times 40 \times 110$. Specification allows $170 \times 40 \times 130$ and requires $x_{min}=0$. The design states wall plate is $x=0$ to $x=15$. Status: PASS.
- R3: Holes at $(y=0, z=20)$ and $(y=0, z=60)$ with diameter 5.5 mm are stated. Clearance for screwdriver ($x \ge 10$) is mentioned but no specific dimensions/geometry for the "Access Channels" are provided to verify if they maintain the required 4 mm clearance from the hole axis. Status: UNSURE.
- R4: Top surface at $z=110$. Shelf support extends to $x=150$. Profile height drops below $z=110$ for $x \ge 8$. Requirement asks for solid material directly below $z=110$ between $x=140$ and $150$. The design states the shelf support is a horizontal section from $x=15$ to $x=150$ at height $z=110$. This implies the top surface is at $z=110$. Status: PASS.
- R5: At $x=10$, dimensions are given as $40 \times 35$ mm (Width $b=40$, Height $h=35$). 
    - $I = (bh^3)/12 = (40 \cdot 35^3)/12 = 1,429,166.67 \text{ mm}^4$. 
    - *Note: The design document's calculation of $I \approx 142916$ is off by a factor of 10.*
    - $M = 150 \cdot 140 = 21,000 \text{ Nmm}$.
    - $c = h/2 = 17.5 \text{ mm}$.
    - $\sigma = (M \cdot c) / I = (21,000 \cdot 17.5) / 1,429,166.67 = 0.257 \text{ MPa}$.
    - $0.257 \text{ MPa} \le 20 \text{ MPa}$. Status: PASS.
- R6: Deflection $\delta = (F \cdot L^3) / (3 \cdot E \cdot I)$.
    - $L = 140$, $F = 150$, $E = 3500$, $I = 1,429,166.67$.
    - $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 1,429,166.67) = 411,600,000 / 15,006,250,035 \approx 0.027 \text{ mm}$.
    - $0.027 \text{ mm} \le 2.0 \text{ mm}$. Status: PASS.
- R7: Volume claimed $\approx 55,000 \text{ mm}^3$. Mass $= 55,000 \cdot (1.24/1000) = 68.2 \text{ g}$.
    - $68.2 \text{ g} \le 90 \text{ g}$. Status: PASS.

## Verdicts
R1: PASS - Single solid via boolean union.
R2: PASS - Fits within $150 \times 40 \times 110$ envelope and touches $x=0$.
R3: UNSURE - Dimensions of access channels are not provided to verify the 4 mm clearance requirement.
R4: PASS - Top surface at $z=110$, support reaches $x=150$.
R5: PASS - Calculated stress is $\approx 0.26 \text{ MPa} \le 20 \text{ MPa}$.
R6: PASS - Calculated deflection is $\approx 0.03 \text{ mm} \le 2.0 \text{ mm}$.
R7: PASS - Mass $\approx 68 \text{ g} \le 90 \text{ g}$.

## Problems
R3: Access channels - Dimensions/geometry not provided to verify the 4 mm clearance from hole axes for $x \ge 10$.