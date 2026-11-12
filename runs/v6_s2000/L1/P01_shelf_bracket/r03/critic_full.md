## Working
- **R1**: The design describes a single solid via boolean operations. PASS.
- **R2**: Envelope: $x \in [0, 150]$ (within $[0, 170]$), $y \in [-20, 20]$, $z \in [10, 110]$ (within $[0, 130]$). Touches wall at $x=0$. PASS.
- **R3**: Holes: diameter 5.5mm ($r=2.75$). Clearance channels: radius 5mm for $x \in [10, 15]$. Requirement asks for no material within 4mm of hole axis for $x \ge 10$. The clearance channel (radius 5mm) covers the region from $x=10$ to $x=15$. However, the requirement says "no material... for $x \ge 10$". The design only provides clearance up to $x=15$. If the screw head or screwdriver requires access beyond $x=15$, it is not specified. But more critically, the clearance channel only exists for $x \in [10, 15]$. For $x > 15$, there is no mention of clearance. However, the requirement says "no material within 4mm... for $x \ge 10$". The design provides a 5mm radius void for $x \in [10, 15]$, but does not provide it for $x > 15$. FAIL.
- **R4**: Top surface: Design says "Top surface is flat at $z=110$ from $x=8$ to $x=150$". However, the Wall Plate height is $z \in [10, 100]$ and the Shelf Arm thickness is $T_z = 6\text{mm}$ or $10\text{mm}$. If the arm is at $z=110$, the bottom of a 10mm thick arm is at $z=100$. The wall plate only goes to $z=100$. There is no mention of a vertical connector between the wall plate ($z=100$) and the shelf arm ($z=110$). If they are not connected, it's not one solid. If they are connected, the dimensions for that connection are missing. Furthermore, the design states "Nothing... above $z=110$ for $x \ge 8$". This is met if the top surface is at $z=110$. PASS/UNSURE (Connectivity depends on missing geometry).
- **R5**: At $x=10$, section is $h=90, w=40$. $I = (w \cdot h^3)/12 = (40 \cdot 90^3)/12 = 2,430,000 \text{ mm}^4$. $c = h/2 = 45 \text{ mm}$. $M = 150\text{ N} \times 140\text{ mm} = 21,000 \text{ Nmm}$. $\sigma = (M \cdot c)/I = (21,000 \cdot 45) / 2,430,000 = 0.388 \text{ MPa}$. $0.388 \le 20$. PASS.
- **R6**: $\delta = (F \cdot L^3)/(3 \cdot E \cdot I)$. $F=150$, $L=140$, $E=3500$, $I=2,430,000$. $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 2,430,000) = 411,600,000 / 25,515,000,000 \approx 0.016 \text{ mm}$. $0.016 \le 2.0$. PASS.
- **R7**: Mass: Design claims $\approx 71.9\text{g}$. This is $< 90\text{g}$. PASS.

## Verdicts
R1: PASS - Single solid via boolean operations.
R2: PASS - Fits within $x[0,150], y[-20,20], z[0,110]$.
R3: FAIL - Clearance channels only extend to $x=15$; requirement requires no material within 4mm for all $x \ge 10$.
R4: UNSURE - Dimensions for the vertical connection between wall plate ($z=100$) and shelf arm ($z=110$) are missing.
R5: PASS - Bending stress is $\approx 0.39$ MPa, which is $\le 20$ MPa.
R6: PASS - Deflection is $\approx 0.016$ mm, which is $\le 2.0$ mm.
R7: PASS - Mass $\approx 71.9$ g is $\le 90$ g.

## Problems
- Screw Access: Clearance channels for R3 only extend from $x=10$ to $x=15$; they must extend for all $x \ge 10$.
- Shelf Connectivity: The wall plate ends at $z=100$ and the shelf arm is at $z=110$; a vertical connector is required to form a single solid.