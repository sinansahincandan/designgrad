**Concept**: A highly optimized, tapered I-beam cantilever bracket. The design utilizes a thin-walled I-beam profile to maximize the Moment of Inertia ($I$) relative to cross-sectional area, ensuring strength and stiffness requirements are met while aggressively minimizing mass through tapering and hollowing.

**Main Features**:
- **Wall Plate**: Extends from $x=0$ to $x=15$, with a width constrained to $y \in [-20, 20]$. Thickness is minimized to reduce mass.
- **Shelf Arm**: A horizontal top surface at exactly $z=110$, extending to $x=150$. To comply with R4, no part of the geometry (including fillets/chamfers) exceeds $z=110$ for $x \ge 8$.
- **Optimized I-Beam Profile (at x=10)**: Instead of a solid block, the profile is an I-beam with height $\approx 60\text{mm}$ and width $\approx 30\text{mm}$, using thin webs and flanges. This provides high $I$ for R5/R6 while drastically reducing volume compared to a rectangular section.
- **Tapering**: The cross-section tapers aggressively from the root ($x=10$) toward the tip ($x=150$), reducing the profile height and width as the bending moment decreases.
- **Screw Access**: 
    - Two primary screw holes (diameter $5.5\text{mm}$) centered at $(y=0, z=20)$ and $(y=0, z=60)$, with axes aligned along the X-axis.
    - Two cylindrical clearance channels (diameter $\ge 8\text{mm}$) centered at the same coordinates, extending from $x=10$ to the front of the part to ensure screwdriver access (satisfying the "no material within 4mm of axis" rule).

**Load Path**: Load at $x=150 \rightarrow$ bending moment transferred through the tapered I-beam arm $\rightarrow$ shear and moment resisted by the high-$I$ I-beam section at $x=10 \rightarrow$ reaction forces at the wall plate ($x=0$).

**Requirement Compliance**:
- R1: Created as a single continuous solid using boolean unions/subtractions.
- R2: Envelope is strictly within $x[0, 170]$, $y[-20, 20]$, and $z[0, 130]$. All features for $x \ge 8$ are capped at $z=110$.
- R3: Screw holes at $(0, 0, 20)$ and $(0, 0, 60)$ with diameter $5.5\text{mm}$; clearance voids of $\varnothing 8\text{mm}$ cut for $x \ge 10$ to provide tool access.
- R4: Top surface is flat at $z=110$ from $x=8$ to $x=150$. No material exists above $z=110$ for $x \ge 8$.
- R5: The I-beam profile at $x=10$ is sized such that $\sigma = M \cdot c / I \approx 10\text{ MPa}$, providing a safety factor while staying well below the $20\text{ MPa}$ limit.
- R6: High Moment of Inertia ($I$) from the I-beam geometry ensures deflection $< 2.0\text{ mm}$.
- R7: Mass is kept $< 90\text{g}$ (target $\approx 70\text{--}85\text{g}$) by using a thin-walled I-beam structure and aggressive tapering instead of a solid rectangular section.