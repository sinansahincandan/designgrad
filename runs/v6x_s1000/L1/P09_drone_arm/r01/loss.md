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