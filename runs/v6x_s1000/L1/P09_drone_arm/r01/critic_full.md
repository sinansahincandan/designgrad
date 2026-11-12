## Working
- R1: The design document claims a single solid via union/lofting. Status: PASS (assumed based on description).
- R2: Envelope: $x \in [0, 130]$ (max $\le 136$), $|y| \le 12$ (max $\le 16$), $z \in [0, 15]$ (height $\le 20$). Status: PASS.
- R3: Holes at $(6, \pm 6)$, diameter $3.2$. Status: PASS.
- R4: Motor holes at $(120 \pm 8, \pm 9.5)$ and shaft hole at $(120, 0)$ with $\varnothing 6$. Status: PASS.
- R5: Bending stress calculation. At $x=20$, the design describes two possible configurations. The first (two $1\times1$ struts spaced $10\text{ mm}$ apart) gives $I \approx 50 \text{ mm}^4$. The second (a single sliver $0.5 \times 2$) gives $I = 0.33 \text{ mm}^4$.
  - Moment at $x=20$: Force $F=12\text{ N}$ at $x=120$, distance to cut is $d = 100\text{ mm}$. $M = F \cdot d = 12 \cdot 100 = 1200 \text{ Nmm}$.
  - Stress $\sigma = M \cdot c / I$.
  - If using the "sliver" ($h=2$, so $c=1$): $\sigma = (1200 \cdot 1) / 0.33 = 3636 \text{ MPa}$. This is much greater than $30 \text{ MPa}$.
  - If using the "dual-strut" ($h=1$, so $c=0.5$): $\sigma = (1200 \cdot 0.5) / 50 = 12 \text{ MPa}$. This passes R5 but fails R6 ($I \le 1.0$).
  - There is no geometry described that satisfies both R5 and R6 simultaneously. Status: FAIL.
- R6: $I$ at $x=20$. The document claims $I = 0.33$ for the sliver, which meets $I \le 1.0$. However, as calculated above, this geometry fails R5. Status: PASS (on the specific value of $I$).
- R7: Mass calculation. Volume $\approx 4000 \text{ mm}^3 = 4 \text{ cm}^3$. Mass $= 4 \cdot 1.24 = 4.96 \text{ g}$. Status: PASS.

## Verdicts
R1: PASS - Single solid via union/lofting.
R2: PASS - $x_{max}=130, y_{max}=12, z_{max}=15$.
R3: PASS - Holes at $(6, \pm 6), \varnothing 3.2$.
R4: PASS - Holes at $(120\pm8, \pm9.5)$ and $(120,0), \varnothing 6$.
R5: FAIL - Stress $\sigma = M c / I$ with $M=1200$, $c=1$, $I=0.33$ results in $3636 \text{ MPa} > 30 \text{ MPa}$.
R6: PASS - $I = 0.33 \le 1.0$.
R7: PASS - Mass $\approx 4.96 \text{ g} \le 20 \text{ g}$.

## Problems
- R5/R6 Conflict: The geometry at $x=20$ cannot satisfy both requirements. To meet R5 ($\sigma \le 30$), the section requires $I/c \ge 40$. To meet R6 ($I \le 1.0$), the section is too weak to support the $12\text{ N}$ load.