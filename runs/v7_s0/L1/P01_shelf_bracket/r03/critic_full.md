## Working
- R1: Design states a single union of primitives. PASS.
- R2: Envelope stated as $x \in [0, 160]$, $y \in [-15, 15]$, $z \in [0, 110]$. This fits within $x \le 170$, $|y| \le 20$, $z \le 130$. PASS.
- R3: Holes at $(0, 0, 20)$ and $(0, 0, 60)$. Clearance cutouts are $10\text{mm} \times 10\text{mm}$ centered on axes from $x=10$ to $x=25$. The distance from the axis to the edge of a $10\text{mm}$ wide cutout is $5\text{mm}$. Since $5\text{mm} > 4\text{mm}$, there is no material within $4\text{mm}$ of the axis for $x \ge 10$. PASS.
- R4: Top surface at $z=110$ extends to $x=160$. Solid material exists between $x=140$ and $150$ (part of the arm). However, the spine is from $x=0$ to $x=15$, height $z=110$. The arm starts at $x=15$. For $x \in [8, 15]$, the spine height is $z=110$. Requirement says "Nothing of the bracket may be above $z=110$ for $x \ge 8$". Since the top surface is exactly at $z=110$, it does not exceed it. PASS.
- R5: At $x=10$, the section is part of the spine. Spine dimensions: $y \in [-15, 15]$ (width $w=30$), $z \in [0, 110]$ (height $h=110$). However, there are screw holes and clearance cutouts.
    - Hole/Cutout at $z=20$: cutout is $10\text{mm}$ high ($z \in [15, 25]$).
    - Hole/Cutout at $z=60$: cutout is $10\text{mm}$ high ($z \in [55, 65]$).
    - The section at $x=10$ is not a simple rectangle. I must recalculate $I$.
    - $I_{total} = (30 \cdot 110^3)/12 = 3,327,500 \text{ mm}^4$.
    - $I_{cutout1} = (10 \cdot 10^3)/12 = 833.3 \text{ mm}^4$ at $z=20$. Using parallel axis theorem: $I_1 = 833.3 + 10(20-55)^2 = 833.3 + 10(1225) = 13,083.3 \text{ mm}^4$ (using centroid of spine at $z=55$).
    - $I_{cutout2} = 833.3 + 10(60-55)^2 = 833.3 + 250 = 1,083.3 \text{ mm}^4$.
    - $I_{net} \approx 3,327,500 - 14,166 = 3,313,334 \text{ mm}^4$.
    - $M = 150\text{N} \cdot 140\text{mm} = 21,000 \text{ Nmm}$.
    - $c = 55\text{mm}$ (distance from center $z=55$ to top/bottom).
    - $\sigma = (21,000 \cdot 55) / 3,313,334 = 0.347 \text{ MPa}$. This is well below $20\text{ MPa}$. PASS.
- R6: $\delta = (F L^3) / (3 E I)$.
    - $L=140$, $F=150$, $E=3500$.
    - $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 3,313,334) = 411,600,000 / 34,789,992,000 \approx 0.0118 \text{ mm}$.
    - This is well below $2.0\text{ mm}$. PASS.
- R7: Volume calculation check.
    - Spine: $15 \cdot 30 \cdot 110 = 49,500 \text{ mm}^3$.
    - Arm: Length from $x=15$ to $x=160$ is $145\text{mm}$.
    - The arm thickness tapers from $20\text{mm}$ at $x=15$ to $5\text{mm}$ at $x=160$.
    - Average thickness $= (20+5)/2 = 12.5\text{mm}$.
    - Arm volume $\approx 145 \cdot 30 \cdot 12.5 = 54,375 \text{ mm}^3$.
    - Total Volume $\approx 49,500 + 54,375 = 103,875 \text{ mm}^3$. (The design document claimed $58,000$, which is incorrect).
    - Mass $= 103,875 \cdot 0.00124 = 128.8 \text{ g}$.
    - This exceeds the limit of $90\text{g}$. FAIL.

## Verdicts
R1: PASS
R2: PASS
R3: PASS
R4: PASS
R5: PASS
R6: PASS
R7: FAIL - Mass is $\approx 128.8\text{g}$ based on dimensions, exceeding $90\text{g}$.

## Problems
- R7: Total mass is $\approx 128.8\text{g}$, must be $\le 90\text{g}$. The spine and arm volumes are too large.