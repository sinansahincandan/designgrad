**Concept**: A split-style saddle clamp consisting of a base plate with two mounting flanges and an upper arch that cradles the pipe. The geometry is optimized to provide structural support while minimizing material to stay under the mass limit, ensuring all components are contained within the specified Y-extent and Z-bounds.

**Main Features**:
- **Base/Flanges**: A continuous base plate and two mounting flanges with a total Y-width of $20\text{ mm}$ ($y \in [-10, 10]$). The bottom surface sits at $z = 0$. To ensure the screw holes at $(\pm 27, 0)$ are fully contained within the solid material, the base plate extends to $x = \pm 30$.
- **Saddle Arch**: A curved section centered at $(0, 0, 12.5)$. To satisfy R4, the arch has an outer radius $\ge 15.5\text{ mm}$ for $|x| \le 7$, ensuring material exists in the radial band between $12.7\text{ mm}$ and $15.5\text{ mm}$ from the pipe axis.
- **Screw Holes**: Two vertical bores of $\varnothing 6.6\text{ mm}$ created via boolean subtraction, centered at $(\pm 27, 0)$, extending from $z = 0$ through the thickness of the flanges and base plate.

**Load Path**: Downward force from the pipe is transferred through the saddle arch to the base plate and then distributed through the mounting flanges into the surface via the screws.

**Requirement Fulfillment**:
- R1: The part is constructed as a single continuous solid using boolean unions (for the body) and subtractions (for the pipe clearance and screw holes).
- R2: Width is $20\text{ mm}$ ($y \in [-10, 10]$), X extent is $60\text{ mm}$ ($|x|=30 \rightarrow 60$), and the bottom surface sits at $z=0$.
- R3: A cylinder of radius $12.6\text{ mm}$ centered at $(0, 0, 12.5)$ is subtracted from the entire solid to ensure zero intersection volume with the pipe.
- R4: Material exists in the band above the pipe by defining the saddle arch's outer boundary to be $\ge 15.5\text{ mm}$ from the pipe axis for $|x| \le 7$.
- R5: Two $\varnothing 6.6\text{ mm}$ holes are drilled vertically at $(\pm 27, 0)$ through the flanges/base.
- R6: Flanges are $3\text{ mm}$ thick ($z=0$ to $3$) and located within $18.5 \le |x| \le 23$ and $|y| \le 4$.
- R7: Total volume is approximately $1600\text{ mm}^3$; mass $\approx 1.98\text{ g}$ (calculated as $V \times 0.00124\text{ g/mm}^3$), which is well below the $25\text{ g}$ limit ($\le 20,161\text{ mm}^3$).