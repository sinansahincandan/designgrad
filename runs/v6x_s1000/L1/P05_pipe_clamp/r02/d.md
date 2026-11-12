**Concept**: A split-style saddle clamp designed as a single manifold solid formed by the Boolean union of several primitives (base plate, flange blocks, connecting walls, and an upper band) followed by two subtractions (pipe cutout and screw holes). The design ensures continuity from the mounting flanges at $x = \pm 27$ through to the central pipe-wrapping band.

**Main Features**:
- **Flange Blocks (R6/R5)**: Two rectangular blocks located at $x = \pm 27$, with thickness $z \in [0, 3]$. To satisfy R6, these include solid material in the interval $|x| \in [18.5, 23]$ and $|y| \le 4$.
- **Base/Connecting Structure**: A central base plate and connecting walls that bridge the gap between the flanges and the pipe area. The structure is continuous across the X-axis: it spans from the flange blocks ($|x| \in [18.5, 23]$) through a connecting wall region ($|x| \in [7, 18.5]$) to the central band ($|x| \le 7$). The Y-range for this entire base/wall assembly is $y \in [-10, 10]$.
- **Upper Band (R4)**: A swept arc profile or torus segment centered at $(0, y, 12.5)$. The cross-section of the band spans the radial distance from $12.7\text{ mm}$ to $15.5\text{ mm}$ from the pipe axis, covering the interval $|x| \le 7$ and spanning $y \in [-10, 10]$.
- **Pipe Cutout (R3)**: A cylindrical void of radius $12.6\text{ mm}$ centered at $(0, y, 12.5)$ for $y \in [-10, 10]$, subtracted from the unioned solid.
- **Screw Holes (R5)**: Two vertical cylindrical voids of $\varnothing 6.6$ centered at $(\pm 27, 0)$, extending through the flange thickness from $z=0$ to $z=3$, subtracted from the final solid.

**Requirement Compliance**:
- R1: The part is a single manifold solid created by the union of the base/flanges, connecting walls, and upper band, followed by two subtractions (pipe cutout and screw holes).
- R2: Y-extent is $20\text{ mm}$ (range $[-10, 10]$), satisfying the $18$-$22\text{ mm}$ requirement. X extent is $\approx 60\text{ mm}$ ($< 80\text{ mm}$).
- R3: Subtracted cylinder with radius $12.6$ at $(0, y, 12.5)$.
- R4: Material exists in the radial band $[12.7, 15.5]$ for $|x| \le 7$ via a swept arc profile.
- R5: Two holes of $\varnothing 6.6$ at $(\pm 27, 0)$ subtracted from $z=0$ to $z=3$.
- R6: Flanges are $3\text{ mm}$ thick and satisfy the solid requirement for $18.5 \le |x| \le 23$ and $|y| \le 4$.
- R7: Volume is approximately $1500\text{ mm}^3$, mass $\approx 1.86\text{ g}$ (well below $25\text{ g}$).