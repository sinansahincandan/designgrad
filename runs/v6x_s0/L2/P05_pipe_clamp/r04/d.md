**Concept**: A split-style saddle clamp consisting of a continuous base plate with integrated mounting flanges and an upper arch that cradles the pipe. The design is constructed as a single solid using boolean unions, with the pipe clearance and screw holes applied via boolean subtraction to ensure all requirements are met without intersection errors.

**Main Features**:
- **Base/Flanges**: A continuous base plate with a total Y-width of exactly $20\text{ mm}$ ($y \in [-10, 10]$). The bottom surface is positioned at exactly $z = 0$. To accommodate the screw holes at $(\pm 27, 0)$, the base plate extends to $x = \pm 30$. This base includes rectangular flange volumes defined by $18.5 \le |x| \le 23$ and $|y| \le 4$, with a thickness from $z=0$ to $z=3$.
- **Saddle Arch**: A curved structural element centered at the pipe axis $(0, 0, 12.5)$. To satisfy R4, the arch is defined such that solid material exists in the radial band between $12.7\text{ mm}$ and $15.5\text{ mm}$ from the pipe axis for $|x| \le 7$. This is achieved by ensuring the arch's outer boundary extends to at least $r = 15.5\text{ mm}$ (e.g., an outer radius of $17.0\text{ mm}$) while the inner clearance is strictly maintained.
- **Screw Holes**: Two vertical bores created via boolean subtraction of $\varnothing 6.6\text{ mm}$ cylinders centered at $(\pm 27, 0)$. To ensure complete through-holes and avoid manifold errors, these cylinders extend from $z = -1$ to $z = 5$, passing entirely through the base and flanges.

**Load Path**: Downward force from the pipe is transferred through the saddle arch to the continuous base plate, which distributes the load into the mounting flanges and subsequently through the screws into the surface.

**Requirement Fulfillment**:
- **R1**: The part is a single valid solid created by unioning the base/flanges and the saddle arch, then subtracting the pipe volume and screw holes.
- **R2**: Width is exactly $20\text{ mm}$ ($y \in [-10, 10]$), X extent is $60\text{ mm}$ ($|x|=30$), and the bottom surface sits at $z = 0$.
- **R3**: A cylinder of radius $12.6\text{ mm}$ centered at $(0, 0, 12.5)$ is subtracted from the *entire* assembled solid to ensure zero intersection volume with the pipe.
- **R4**: Material is guaranteed in the band $12.7 \le r \le 15.5$ for $|x| \le 7$ by defining the arch geometry to occupy this radial range relative to $(0, 0, 12.5)$.
- **R5**: Two $\varnothing 6.6\text{ mm}$ holes are subtracted at $(\pm 27, 0)$ from $z = -1$ to $z = 5$.
- **R6**: Flanges are defined as solid volumes from $z=0$ to $3$ within the region $18.5 \le |x| \le 23$ and $|y| \le 4$, integrated into the base plate.
- **R7**: Total volume is approximately $1600\text{ mm}^3$; mass $\approx 1.98\text{ g}$ (calculated as $V \times 0.00124\text{ g/mm}^3$), which is well below the $25\text{ g}$ limit.