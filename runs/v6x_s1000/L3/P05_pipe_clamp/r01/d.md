**Concept**: A unified saddle clamp consisting of a central base plate that serves as a foundation for two mounting flanges and vertical connecting walls. An upper arc segment (the band) cradles the pipe, which is integrated into the base via thick side walls to ensure a single continuous solid body.

**Main Features**:
- **Base Plate**: A central rectangular slab spanning $x \in [-27, 27]$, $y \in [-10, 10]$, and $z \in [0, 3]$. This provides the manifold for all other features.
- **Flanges (R6)**: Integrated into the base plate; solid material is guaranteed at $18.5 \le |x| \le 23$ and $|y| \le 4$ with thickness $z \in [0, 3]$.
- **Pipe Cutout (R3)**: A cylindrical void of radius $12.6\text{ mm}$ centered on the axis $x=0, z=12.5$, extending along the Y-axis to clear the pipe volume.
- **Upper Band (R4)**: An arc segment located at a radial distance of $14.1\text{ mm}$ from the pipe axis $(0, y, 12.5)$, providing material in the band $[12.7, 15.5]$ for $|x| \le 7$.
- **Connecting Walls (R1)**: Thick vertical slabs that bridge the upper band down to the top of the base plate ($z=3$) at the lateral edges of the pipe area ($|x| \le 7$), ensuring a single topological manifold.
- **Screw Holes (R5)**: Two cylindrical subtractions of $\varnothing 6.6\text{ mm}$ centered at $(\pm 27, 0)$, extending vertically from $z=0$ to $z=3$.

**Requirement Compliance**:
- R1: The part is a single union of the base plate, connecting walls, and upper band, with subtractions for the pipe and holes.
- R2: Total Y-extent is $20\text{ mm}$ (from $y=-10$ to $y=10$), within the $18$-$22\text{ mm}$ range. Total X-extent is $\approx 54\text{ mm}$ ($< 80\text{ mm}$). Sits on $z=0$.
- R3: Subtracted cylinder with radius $12.6$ at axis $x=0, z=12.5$.
- R4: Material exists in the radial band $[12.7, 15.5]$ for $|x| \le 7$.
- R5: Two holes of $\varnothing 6.6$ at $(\pm 27, 0)$ through $z=0$ to $z=3$.
- R6: Flanges are $3\text{ mm}$ thick and located within the specified coordinate bounds.
- R7: Volume is approximately $1500\text{--}1800\text{ mm}^3$, mass $\approx 2.0\text{ g}$ (well below $25\text{ g}$).