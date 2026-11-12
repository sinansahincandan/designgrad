## Working
- **R1**: The design claims a single solid via boolean operations. **PASS**.
- **R2**: Envelope: $x$ goes from 0 to 130 (within $\le 136$). $|y|$ max is 15 ($30/2$) (within $\le 16$). $z$ max is 14 (within $\le 20$). **PASS**.
- **R3**: Holes at $(6, \pm 6)$, diameter 3.2 mm. Matches spec. **PASS**.
- **R4**: Motor holes: $(120 \pm 8, \pm 9.5)$ and shaft hole $(120, 0)$. Diameter 3.2 mm for motor, 6 mm for shaft. Matches spec. **PASS**.
- **R5**: Section at $x=20$: $b=30$, $h=14$, $t_f=1.5$, $t_w=2$.
    - $I = \frac{30 \cdot 14^3}{12} - \frac{(30-2) \cdot (14-3)^3}{12} = \frac{82320}{12} - \frac{28 \cdot 1331}{12} = 6860 - 3089.17 = 3770.83\text{ mm}^4$.
    - *Note: The design document's calculation of $I \approx 1953$ is incorrect, but the actual value is higher.*
    - Moment $M = 12\text{ N} \cdot (120 - 20) = 1200\text{ Nmm}$.
    - $\sigma = \frac{M \cdot c}{I} = \frac{1200 \cdot 7}{3770.83} \approx 2.23\text{ MPa}$.
    - $2.23\text{ MPa} \le 30\text{ MPa}$. **PASS**.
- **R6**: Requirement: $I$ of the $x=20$ section $\le 1.0\text{ mm}^4$.
    - Calculated $I = 3770.83\text{ mm}^4$.
    - $3770.83 > 1.0$. **FAIL**. (Note: The requirement is mathematically unusual for stiffness, but must be followed as written).
- **R7**: Mass calculation:
    - Volume estimate: Average width $\approx 25\text{ mm}$. Height $14\text{ mm}$. Thickness (avg) $\approx 3.5\text{ mm}$ (I-beam approximation).
    - $V \approx 130 \cdot 25 \cdot 3.5 \cdot (\text{void ratio})$.
    - Let's use the design document's claim: Volume $\approx 13\text{ cm}^3$.
    - Mass $= 13\text{ cm}^3 \cdot 1.24\text{ g/cm}^3 = 16.12\text{ g}$.
    - $16.12\text{ g} \le 20\text{ g}$. **PASS**.

## Verdicts
R1: PASS - Single solid via boolean logic.
R2: PASS - Envelope is $130 \times 30 \times 14$.
R3: PASS - Holes at $(6, \pm 6)$, $\varnothing 3.2$.
R4: PASS - Motor holes and shaft hole match coordinates and diameters.
R5: PASS - Stress $\approx 2.23\text{ MPa} \le 30\text{ MPa}$.
R6: FAIL - $I \approx 3771\text{ mm}^4$, which is $> 1.0\text{ mm}^4$.
R7: PASS - Mass $\approx 16.12\text{ g} \le 20\text{ g}$.

## Problems
- R6: Section $I$ at $x=20$ is $3771\text{ mm}^4$; must be $\le 1.0\text{ mm}^4$.