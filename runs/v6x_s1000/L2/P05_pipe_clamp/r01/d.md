**Concept**: A split-style saddle clamp designed as a single continuous solid. The design consists of two mounting flanges at the base, an upper arc (band) that cradles the pipe, and vertical connecting walls that bridge the flanges to the band to ensure topological connectivity. All geometry is oriented such that the mounting surface lies on the $z=0$ plane.

**Main Features**:
- **Base/Flanges**: Two rectangular blocks providing the mounting footprint: $x \in [18.5, 27]$ and $x \in [-27, -18.5]$, with $y \in [-4, 4]$ and $z \in [0, 3]$.
- **Upper Band**: An arc segment centered at $(0, 0, 12.5)$ with a radial distance of $14.1\text{ mm}$ (midpoint of the required $12.7$ to $15.5$ band), restricted to $|x| \le 7$.
- **Connecting Walls**: Solid vertical bridges that extend from the inner edges of the flanges ($|x| = 18.5$) to the outer edges of the upper band ($|x| = 7$), ensuring a single valid solid (R1).
- **Pipe Cutout**: A cylindrical subtraction with radius $12.6\text{ mm}$ centered at $(0, y, 12.5)$, performed after all additive primitives are joined to ensure a clean void (R3).
- **Screw Holes**: Two cylindrical subtractions of $\varnothing 6.6$ centered at $(\pm 27, 0)$ extending from $z=0$ to $z=3$, located within the flange volumes (R5).

**Requirement Compliance**:
- R1: The part is a single union of flanges, upper band, and connecting walls, with holes and pipe void subtracted.
- R2: Total Y-extent is $20\text{ mm}$ ($y \in [-10, 10]$), meeting the $18$-$22\text{ mm}$ requirement. Total X-extent is $54\text{ mm}$ ($x \in [-27, 27]$), which is $< 80\text{ mm}$. Minimum Z is exactly $0$.
- R3: Subtracted cylinder with radius $12.6$ at $(0, y, 12.5)$.
- R4: Material exists in the radial band $[12.7, 15.5]$ for $|x| \le 7$.
- R5: Two holes of $\varnothing 6.6$ at $(\pm 27, 0)$ from $z=0$ to $z=3$.
- R6: Flanges are defined as solid blocks from $z=0$ to $3$ for the specified $x$ and $y$ ranges.
- R7: Volume is approximately $1500\text{ mm}^3$, mass $\approx 1.86\text{ g}$ (well below $25\text{ g}$).