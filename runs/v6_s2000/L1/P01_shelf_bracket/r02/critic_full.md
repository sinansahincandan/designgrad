## Working
- **R1**: The design describes a single solid formed via boolean operations. PASS.
- **R2**: Envelope: $x \in [0, 150]$, $y \in [-20, 20]$, $z \in [0, 110]$. Max $x=150 \le 170$, max $y=20$, max $z=110 \le 130$. Touches wall at $x=0$. PASS.
- **R3**: Holes diameter 5.5mm (radius 2.75mm). Clearance channels radius 5mm for $x \in [10, 15]$. Requirement: no material within 4mm of hole axis for $x \ge 10$. The clearance channel radius is 5mm, which is $> 4$mm. However, the holes are centered at $(y=0, z=20)$ and $(y=0, z=60)$. The design states the wall plate extends from $x=0$ to $x=15$. If the hole axis is along X, it passes through the wall. The clearance channel starts at $x=10$. Since 5mm $> 4$mm, the screwdriver access requirement is met for $x \in [10, 15]$. PASS.
- **R4**: Top surface at $z=110$ from $x=8$ to $x=150$. Solid material below $z=110$ between $x=140$ and $150$ is the shelf arm ($T_z = 10\text{mm}$). No material above $z=110$ for $x \ge 8$ (arm ends at $z=110$). PASS.
- **R5**: Section at $x=10$: The design claims a rectangular section $h=90$, $w=40$. However, the Wall Plate width is $y \in [-20, 20]$ ($w=40$) and height $z \in [0, 110]$. The Shelf Arm is at $z \in [100, 110]$. At $x=10$, these overlap. Total height $h = 110$. But the design specifically claims a "deep rectangular section with height $h=90\text{mm}$ and width $w=40\text{mm}$". Let's use the claimed dimensions for the calculation:
    - $M = 150\text{ N} \times 140\text{ mm} = 21,000\text{ Nmm}$.
    - $I = (w \cdot h^3) / 12 = (40 \cdot 90^3) / 12 = 2,430,000\text{ mm}^4$.
    - $c = h/2 = 45\text{ mm}$.
    - $\sigma = M \cdot c / I = (21,000 \times 45) / 2,430,000 = 945,000 / 2,430,000 \approx 0.389\text{ MPa}$.
    - $0.389\text{ MPa} \le 20\text{ MPa}$. PASS.
- **R6**: Stiffness:
    - $E = 3500\text{ MPa}$.
    - $\delta = (F \cdot L^3) / (3 \cdot E \cdot I) = (150 \times 140^3) / (3 \times 3500 \times 2,430,000)$.
    - $\delta = 411,600,000 / 25,515,000,000 \approx 0.016\text{ mm}$.
    - $0.016\text{ mm} \le 2.0\text{ mm}$. PASS.
- **R7**: Mass:
    - Volume calculation check:
        - Wall Plate: $15 \times 40 \times 110 = 66,000\text{ mm}^3$.
        - Shelf Arm (from $x=15$ to $x=150$): $135 \times 40 \times 10 = 54,000\text{ mm}^3$.
        - Total Volume $\approx 120,000\text{ mm}^3 = 120\text{ cm}^3$.
    - Mass $= 120\text{ cm}^3 \times 1.24\text{ g/cm}^3 = 148.8\text{ g}$.
    - The design document claims $V \approx 65\text{ cm}^3$ and mass $\approx 80.6\text{g}$, but the dimensions provided ($x=15, y=40, z=110$ for wall; $x=135, y=40, z=10$ for arm) result in a much higher volume.
    - Even subtracting screw holes (negligible), the mass is $\approx 148\text{g}$, which is $> 90\text{g}$. FAIL.

## Verdicts
R1: PASS
R2: PASS
R3: PASS
R4: PASS
R5: PASS
R6: PASS
R7: FAIL - Mass is $\approx 148.8\text{ g}$ based on provided dimensions, exceeding $90\text{ g}$.

## Problems
- R7: Mass is $\approx 148.8\text{ g}$, must be $\le 90\text{ g}$.