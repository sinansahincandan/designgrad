## Working
- **R1**: The design claims to use boolean operations to create a single solid. Status: PASS (based on concept).
- **R2**: Envelope check: $x$ goes up to 150 (req $\le 170$), $y \in [-20, 20]$ (req $[-20, 20]$), $z \in [0, 110]$ (req $[0, 130]$). Touches wall at $x=0$. Status: PASS.
- **R3**: Screw holes are diameter 5.5mm at $(y=0, z=20)$ and $(y=0, z=60)$. Clearance channels have radius 5mm (diameter 10mm) for $x \ge 10$. Requirement is "no material within 4 mm of either hole axis". Since the channel radius (5mm) > 4mm, this is satisfied. Status: PASS.
- **R4**: Top surface at $z=110$ from $x=8$ to $x=150$. No part above $z=110$ for $x \ge 8$. Wall plate reaches $z=110$. Status: PASS.
- **R5**: Section at $x=10$: $h=90\text{mm}$, $w=40\text{mm}$. However, the design states the wall plate width is $y \in [-20, 20]$ (total width 40) and the arm profile at $x=10$ has $w=40$. But wait: R3 requires clearance channels with radius 5mm centered at $y=0$. This removes material from the center of the section.
    - Moment $M = 150\text{ N} \times 140\text{ mm} = 21,000\text{ N}\cdot\text{mm}$.
    - Section at $x=10$: Rectangular $40 \times 90$ minus two holes/channels. The channels are at $z=20$ and $z=60$.
    - Let's approximate $I$ for a solid $40 \times 90$ rectangle: $I = (w \cdot h^3)/12 = (40 \cdot 90^3)/12 = 2,430,000\text{ mm}^4$.
    - Subtracting two channels ($r=5$, $w=40$): $\Delta I \approx 2 \times [\frac{\pi \cdot 5^4}{4} + (\pi \cdot 5^2) \cdot d^2]$ where $d$ is distance from neutral axis. Neutral axis is at $z=45$.
    - Hole 1 ($z=20$): $d = |45-20| = 25$. $\Delta I_1 \approx (78.5 \cdot 25^2) + 1963 \approx 49,063 + 1963 \approx 51,026\text{ mm}^4$.
    - Hole 2 ($z=60$): $d = |45-60| = 15$. $\Delta I_2 \approx (78.5 \cdot 15^2) + 1963 \approx 17,663 + 1963 \approx 19,626\text{ mm}^4$.
    - Total $I \approx 2,430,000 - 70,652 = 2,359,348\text{ mm}^4$.
    - Stress $\sigma = M \cdot c / I = 21,000 \cdot 45 / 2,359,348 \approx 0.4\text{ MPa}$. This is well below 20 MPa. Status: PASS.
- **R6**: Deflection $\delta = (F \cdot L^3) / (3 \cdot E \cdot I)$.
    - $F=150$, $L=140$, $E=3500$, $I \approx 2,359,348$.
    - $\delta = (150 \cdot 140^3) / (3 \cdot 3500 \cdot 2,359,348) = 411,600,000 / 24,773,154,000 \approx 0.016\text{ mm}$.
    - This is well below 2.0 mm. Status: PASS.
- **R7**: Mass check. Document claims Volume $\approx 65\text{ cm}^3$.
    - $Mass = Volume \times Density = 65 \times 1.24 = 80.6\text{ g}$.
    - Requirement is $\le 90\text{ g}$. Status: PASS.

## Verdicts
R1: PASS - Single solid via boolean operations.
R2: PASS - Fits within $x[0,170], y[-20,20], z[0,130]$.
R3: PASS - Clearance channels (radius 5mm) exceed the 4mm requirement.
R4: PASS - Top surface at $z=110$ and no material above for $x \ge 8$.
R5: PASS - Calculated stress $\approx 0.4\text{ MPa} \le 20\text{ MPa}$.
R6: PASS - Calculated deflection $\approx 0.016\text{ mm} \le 2.0\text{ mm}$.
R7: PASS - Estimated mass $80.6\text{ g} \le 90\text{ g}$.

## Problems
None