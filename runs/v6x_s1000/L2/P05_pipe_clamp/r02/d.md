**Concept**: A single-body split-style saddle clamp. The design consists of a continuous base plate that spans the entire width and length, an upper arc segment (clamp band) that cradles the pipe, and vertical connecting walls that bridge the two to ensure a single solid manifold.

**Main Features**:
- **Base Plate**: A single continuous block spanning $x \in [-27, 27]$, $y \in [-10, 10]$, and $z \in [0, 3]$. This provides the foundation for the flanges and connects the screw hole regions to the central body.
- **Flanges (R6)**: Integrated into the base plate at $|x| \in [18.5, 23]$ and $y \in [-4, 4]$, with a thickness of $3\text{ mm}$ ($z \in [0, 3]$).
- **Screw Holes (R5)**: Two cylindrical subtractions of $\varnothing 6.6$ centered at $(\pm 27, 0)$, extending from $z=0$ to $z=3$. These are located within the base plate extensions.
- **Pipe Cutout (R3)**: A cylindrical void with radius $12.6\text{ mm}$ centered on the pipe axis $(x=0, z=12.5)$, extending along the Y-axis.
- **Upper Band (R4)**: An arc segment defined by a radial distance from the pipe axis $(0, y, 12.5)$ in the range $r \in [12.7, 15.5]$. This band covers $|x| \le 7$ and spans the full width $y \in [-10, 10]$.
- **Connecting Walls**: Vertical solid walls that bridge the base plate ($z=3$) to the upper band, ensuring R1 (single valid solid) is satisfied.

**Requirement Compliance**:
- R1: Constructed as a single union of the base, connecting walls, and upper band, with screw holes and pipe void subtracted.
- R2: Total Y-extent is $20\text{ mm}$ ($y \in [-10, 10]$), which is within the $18$-$22\text{ mm}$ range. Total X-extent is $\approx 54\text{ mm}$ ($< 80\text{ mm}$). Sits on $z=0$.
- R3: Subtracted cylinder with radius $12.6$ at $(0, y, 12.5)$.
- R4: Material exists in the radial band $[12.7, 15.5]$ for $|x| \le 7$, spanning $y \in [-10, 10]$.
- R5: Two holes of $\varnothing 6.6$ at $(\pm 27, 0)$ from $z=0$ to $z=3$.
- R6: Flange regions ($|x| \in [18.5, 23], |y| \le 4$) are part of the $3\text{ mm}$ thick base plate.
- R7: Volume is well within limits for a mass $< 25\text{ g}$ using PLA (density $1.24\text{ g/cm}^3$).