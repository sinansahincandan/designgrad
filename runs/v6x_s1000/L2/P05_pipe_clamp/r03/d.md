**Concept**: A single-body split-style saddle clamp. The design consists of an expanded continuous base plate, a central solid block (connecting walls) that bridges the base to the upper band, and an upper arc segment (clamp band) that cradles the pipe, ensuring a single manifold solid.

**Main Features**:
- **Base Plate**: A single continuous block spanning $x \in [-30, 30]$, $y \in [-10, 10]$, and $z \in [0, 3]$. This expanded footprint ensures that the screw hole regions at $(\pm 27, 0)$ are fully encased within solid material.
- **Flanges (R6)**: Integrated into the base plate at $|x| \in [18.5, 23]$ and $y \in [-4, 4]$, with a thickness of $3\text{ mm}$ ($z \in [0, 3]$), ensuring continuous solid material for requirement R6.
- **Screw Holes (R5)**: Two cylindrical subtractions of $\varnothing 6.6$ centered at $(\pm 27, 0)$, extending from $z=0$ to $z=3$. These are now correctly located within the expanded base plate.
- **Pipe Cutout (R3)**: A cylindrical void with radius $12.6\text{ mm}$ centered on the pipe axis $(x=0, z=12.5)$, extending along the Y-axis ($y \in [-10, 10]$).
- **Upper Band (R4)**: An arc segment defined by a radial distance from the pipe axis $(0, y, 12.5)$ in the range $r \in [12.7, 15.5]$. This band covers $|x| \le 7$ and spans the full width $y \in [-10, 10]$.
- **Connecting Walls**: Two solid blocks spanning $x \in [-7, 7]$ and $y \in [-10, 10]$, extending from the top of the base plate ($z=3$) to the bottom of the upper band ($z \approx 12.7$). This ensures a continuous union between the base and the band (R1).

**Requirement Compliance**:
- R1: Constructed as a single union of the expanded base, the solid connecting walls, and the upper band, with screw holes and pipe void subtracted.
- R2: Total Y-extent is exactly $20\text{ mm}$ ($y \in [-10, 10]$), which is within the $18$-$22\text{ mm}$ range. Total X-extent is $60\text{ mm}$ ($< 80\text{ mm}$). Sits on $z=0$.
- R3: Subtracted cylinder with radius $12.6$ at $(0, y, 12.5)$.
- R4: Material exists in the radial band $[12.7, 15.5]$ for $|x| \le 7$, spanning $y \in [-10, 10]$.
- R5: Two holes of $\varnothing 6.6$ at $(\pm 27, 0)$ from $z=0$ to $z=3$, fully contained within the base plate.
- R6: Flange regions ($|x| \in [18.5, 23], |y| \le 4$) are part of the $3\text{ mm}$ thick continuous solid base plate.
- R7: Volume is well within limits for a mass $< 25\text{ g}$ using PLA (density $1.24\text{ g/cm}^3$).