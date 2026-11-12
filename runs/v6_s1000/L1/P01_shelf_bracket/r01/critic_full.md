## Working
- R1: The design claims a single solid via boolean operations. **PASS**.
- R2: Envelope stated as $150 \times 40 \times 110$. Limits are $x=170, y=\pm20, z=130$. Fits. Touches wall at $x=0$ (Wall plate starts at $x=0$). **PASS**.
- R3: Holes diameter 5.5mm at $(y=0, z=20)$ and $(z=60)$. Access channels are $10 \times 10$ mm centered on axes from $x=10$ to $x=15$. The distance from the axis to the edge of a $10 \times 10$ cutout is $5\text{ mm}$. Since $5 > 4$, the clearance requirement for $x \ge 10$ is met. **PASS**.
- R4: Top surface at $z=110$. Shelf support reaches $x=150$. Profile height drops below $z=110$ for $x \ge 8$. However, the wall plate extends from $x=0$ to $x=15$, and its height is stated as $z=0$ to $z=120$. If the wall plate goes up to $z=120$, it violates "Nothing of the bracket may be above $z = 110$ for $x \ge 8$". **FAIL**.
- R5: Section at $x=10$: The design claims a rectangle $40 \times 35$. However, the wall plate is $x=0$ to $x=15$, and the shelf support starts at $x=15$. At $x=10$, only the wall plate exists. The wall plate dimensions are given as $y$-span (implied by envelope/R2) and $z=0$ to $120$. If it is a rectangle, width is not explicitly stated in the "Main Features" but R2 implies $y \in [-20, 20]$ (width 40). If height is $120$, then at $x=10$, the section is $40 \times 120$. The design claims $40 \times 35$ for stress calculation. Without the exact geometry of the "tapered profile" and the wall plate thickness/width, I cannot verify the cross-section at $x=10$. **UNSURE**.
- R6: Deflection depends on $I$ at $x=10$. Since $I$ is unknown due to lack of specific dimensions for the taper and wall plate width, this cannot be verified. **UNSURE**.
- R7: Mass calculation relies on volume. Volume is stated as "approx $55,000 \text{ mm}^3$". This is an estimate provided by the designer, not a derived value from specific geometry. Without explicit dimensions for all parts (width of wall plate, thickness of shelf support, exact taper function), I cannot calculate the volume. **UNSURE**.

## Verdicts
R1: PASS - Single solid via boolean union.
R2: PASS - $150 \times 40 \times 110$ fits within $170 \times 40 \times 130$.
R3: PASS - $10\text{ mm}$ cutout provides $5\text{ mm}$ clearance, which is $> 4\text{ mm}$.
R4: FAIL - Wall plate height $z=120$ exceeds the limit of $z=110$ for $x \ge 8$.
R5: UNSURE - Cross-section dimensions at $x=10$ are not explicitly defined.
R6: UNSURE - Moment of inertia $I$ at $x=10$ cannot be calculated without explicit geometry.
R7: UNSURE - Volume/Mass cannot be verified without explicit dimensions for all features.

## Problems
- R4: Wall plate height is $z=120$; must be $\le 110$ for $x \ge 8$.
- R5, R6, R7: Missing specific dimensions for the wall plate width, shelf support thickness, and taper profile to allow verification of stress, stiffness, and mass.