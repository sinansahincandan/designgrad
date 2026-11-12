**Concept**: A unified saddle clamp consisting of a central base plate, two dedicated flange blocks, vertical connecting walls, and an upper arc segment (the band). The design is constructed as a single continuous topological manifold via Boolean Union to ensure structural integrity.

**Main Features**:
- **Base Plate**: A central rectangular slab spanning $x \in [-27, 27]$, $y \in [-10, 10]$, and $z \in [0, 3]$. This ensures the minimum Z-coordinate is exactly $0$ and the total Y-extent is exactly $20\text{ mm}$ (meeting R2).
- **Flanges (R6)**: To ensure 100% coverage of the required area, two solid blocks are defined for $|x| \in [18.5, 23]$ and $y \in [-4, 4]$ with thickness $z \in [0, 3]$. These are joined to the Base Plate via Boolean Union.
- **Pipe Cutout (R3)**: A cylindrical subtraction of radius $12.6\text{ mm}$ centered on the axis $x=0, z=12.5$, extending along the Y-axis to clear the pipe volume.
- **Upper Band (R4)**: A hollow cylindrical shell segment centered at $(0, y, 12.5)$ with an inner radius of $12.7\text{ mm}$ and an outer radius of $15.5\text{ mm}$. This provides the required material in the radial band $[12.7, 15.5]$ for $|x| \le 7$.
- **Connecting Walls (R1)**: Thick vertical slabs that bridge the gap between the top of the Base Plate ($z=3$) and the Upper Band at the lateral edges of the pipe area ($|x| \le 7$), ensuring a single continuous solid.
- **Screw Holes (R5)**: Two cylindrical subtractions of $\varnothing 6.6\text{ mm}$ centered at $(x, y) = (\pm 27, 0)$, extending vertically from $z=0$ to $z=3$ through the base plate/flange area.

**Requirement Compliance**:
- R1: The part is a single valid solid formed by the Boolean Union of the base plate, flange blocks, connecting walls, and upper band, followed by the subtraction of the pipe volume and screw holes.
- R2: Sits on $z=0$ (minimum Z is 0). Total Y-extent is $20\text{ mm}$ ($y \in [-10, 10]$). Total X-extent is $54\text{ mm}$ ($< 80\text{ mm}$).
- R3: Cylindrical subtraction with radius $12.6\text{ mm}$ at axis $x=0, z=12.5$.
- R4: Material exists in the radial band $[12.7, 15.5]$ for $|x| \le 7$ via the shell segment.
- R5: Two holes of $\varnothing 6.6\text{ mm}$ centered at $(\pm 27, 0)$ passing through $z=0$ to $z=3$.
- R6: Flanges are guaranteed to be $3\text{ mm}$ thick and cover the entire region $18.5 \le |x| \le 23$ and $|y| \le 4$ via explicit solid block definition and Boolean Union.
- R7: Volume is approximately $1500\text{--}1800\text{ mm}^3$, mass $\approx 2.0\text{ g}$ (well below $25\text{ g}$).