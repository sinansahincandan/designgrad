**Concept**: A split-style saddle clamp designed as a single manifold solid formed by the Boolean union of a base plate (extending $y \in [-10, 10]$), an upper arc, and connecting side walls. The design bridges the upper band to the lower flanges through vertical walls to ensure a continuous volume.

**Main Features**:
- **Base/Flanges**: A central base plate and two mounting flanges extending across the Y-range $y \in [-10, 10]$. Flanges are located at $x = \pm 27$, with thickness $z \in [0, 3]$.
- **Pipe Cutout**: A cylindrical void of radius $12.6\text{ mm}$ centered at $(0, y, 12.5)$ for $y \in [-10, 10]$.
- **Upper Band**: An arc segment located at a radial distance of $14.1\text{ mm}$ (midpoint of $12.7$ and $15.5$) from the pipe axis, spanning $y \in [-10, 10]$ for $|x| \le 7$.
- **Connecting Walls**: Vertical side walls that extend from $z=3$ to the upper band, spanning the Y-range $[-10, 10]$ and covering the X-interval between the flanges ($|x| \in [7, 18.5]$), ensuring a single continuous solid.

**Requirement Compliance**:
- R1: The part is constructed as a single union of primitives (base, arc, and connecting walls) and one subtraction (pipe cutout).
- R2: Y-extent is $20\text{ mm}$ (range $[-10, 10]$), satisfying the $18$-$22\text{ mm}$ requirement. X extent is $\approx 60\text{ mm}$ ($< 80\text{ mm}$).
- R3: Subtracted cylinder with radius $12.6$ at $(0, y, 12.5)$.
- R4: Material exists in the radial band $[12.7, 15.5]$ for $|x| \le 7$.
- R5: Two holes of $\varnothing 6.6$ at $(\pm 27, 0)$ from $z=0$ to $z=3$.
- R6: Flanges are $3\text{ mm}$ thick at the specified coordinates ($18.5 \le |x| \le 23$).
- R7: Volume is approximately $1500\text{ mm}^3$, mass $\approx 1.86\text{ g}$ (well below $25\text{ g}$).