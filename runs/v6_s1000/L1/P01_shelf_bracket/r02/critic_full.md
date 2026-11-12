## Working
- R1: The design claims a single solid via boolean union/subtraction. PASS.
- R2: Envelope: $x$ goes 0 to 150 (within 170), $y$ is $\pm 20$ ($\Delta y=40$, within -20 to 20), $z$ goes 0 to 110 (within 130). Touches wall at $x=0$. PASS.
- R3: Holes at $(0, 20)$ and $(0, 60)$. Access channels are $20 \times 15$ centered on axes from $x=10$ to $x=20$. The requirement states "no material within 4 mm of either hole axis for $x \ge 10$". If the channel is $20\text{ mm}$ wide (Y-direction) and $15\text{ mm}$ high (Z-direction), the distance from the axis to the nearest edge in Z is $7.5\text{ mm}$, which is $> 4\text{ mm}$. However, the channel only extends to $x=20$. The requirement says "for $x \ge 10$". This implies for *all* $x \ge 10$, there must be no material within 4mm of the axis. The design only provides clearance from $x=10$ to $x=20$. For $x > 20$, the material returns to the full thickness/width. Since the hole axis is at $y=0, z=20$ and $z=60$, we must check if there is material within 4mm of these axes for $x > 20$. The design states the tapered profile starts at $x=10$ with height $H(x)$. At $x=20$, $H(20) = 35 - (25/140)(10) \approx 33.2\text{ mm}$. If the shelf is at $z=110$ and the arm thickness is $\sim 33\text{ mm}$, the bottom of the arm is at $z \approx 77$. The hole axis at $z=60$ is below the arm for $x > 20$. However, the requirement says "no material within 4mm of either hole axis for $x \ge 10$". This means the holes must be open/clear to the front. If the holes are only in the wall plate ($x=0$ to $15$), and the access channels only go to $x=20$, then for $x > 20$, there is no hole, but there *is* material (the arm). The requirement "no material within 4mm of either hole axis" refers to the space around the infinite line defined by the axis. If the holes are intended to be through-holes or if the screwdriver must reach them, the design fails because for $x > 20$, there is solid material (the arm) occupying the space where the hole axes would be. Wait, the requirement says "A screwdriver must reach each screw head from the front: no material within 4 mm of either hole axis for x >= 10". This means at any point $x \ge 10$, if you look at the cross section, there should be a void of radius 4mm around $(y=0, z=20)$ and $(y=0, z=60)$. The design provides this only for $x \in [10, 20]$. For $x > 20$, the arm is solid. FAIL.
- R4: Top surface at $z=110$. Arm reaches $x=150$. Solid material below $z=110$ between $x=140$ and $150$ around $y=0$: The arm exists there. No part above $z=110$ for $x \ge 8$: Wall plate is capped at $z=110$. PASS.
- R5: At $x=10$, $\Delta y = 40, \Delta z = 35$. $I = (40 \cdot 35^3)/12 = 142,916.67\text{ mm}^4$. $M = 150 \cdot 140 = 21,000\text{ Nmm}$. $c = 17.5\text{ mm}$. $\sigma = (21,000 \cdot 17.5) / 142,916.67 = 2.55\text{ MPa} \le 20\text{ MPa}$. PASS.
- R6: $E = 3500\text{ MPa}, L=140, I=142,916.67$. $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 142,916.67) = 411,600,000 / 1,500,625,035 \approx 0.27\text{ mm} \le 2.0\text{ mm}$. PASS.
- R7: Volume calculation: Wall plate $15 \cdot 40 \cdot 110 = 66,000$. Arm (tapered) $x=15$ to $150$ (length 135). Height at $x=15$: $H(15) = 35 - (25/140)(5) \approx 34.1\text{ mm}$. Height at $x=150$: $H(150) = 10\text{ mm}$. Average height $\approx 22.05\text{ mm}$. Volume arm $\approx 135 \cdot 40 \cdot 22.05 = 119,070$. Total volume $\approx 66,000 + 119,070 = 185,070\text{ mm}^3$. Mass $= 185,070 \cdot (1.24 / 1000) = 229.4\text{ g}$. This is $> 90\text{ g}$. FAIL.

## Verdicts
R1: PASS
R2: PASS
R3: FAIL - Material exists within 4mm of hole axes for $x > 20$.
R4: PASS
R5: PASS
R6: PASS
R7: FAIL - Mass is $\approx 229\text{ g}$, which is $> 90\text{ g}$.

## Problems
- R7: Mass is $\approx 229\text{ g}$; must be $\le 90\text{ g}$ (requires volume reduction to $\le 72,580\text{ mm}^3$).
- R3: Access channels only extend to $x=20$; must extend for all $x \ge 10$ where the hole axis exists to ensure screwdriver clearance.