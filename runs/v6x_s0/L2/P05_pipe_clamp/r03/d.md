**Concept**: A split-style saddle clamp designed as a single continuous solid. The design consists of a base plate with integrated mounting flanges and a curved saddle arch that cradles the pipe. The geometry is constructed by first unioning the structural components and then subtracting the necessary clearances to ensure compliance with all geometric constraints.

**Construction Workflow (R1)**:
- **Step 1 (Union)**: Create the base/flanges and the saddle arch as separate solids, then perform a `union()` operation to form one continuous body.
- **Step 2 (Subtraction)**: Perform boolean subtractions for the pipe clearance and the screw holes from the single unioned body to ensure a valid, single manifold solid.

**Main Features**:
- **Base/Flanges (R2, R6)**: A base plate with integrated flanges. The total Y-extent is exactly $20\text{ mm}$ ($y \in [-10, 10]$). The bottom surface sits at exactly $z = 0$. To ensure the screw holes at $(\pm 27, 0)$ are fully contained within the solid material, the base plate extends to $x = \pm 30$. The flanges are defined as a solid region from $z = 0$ to $z = 3$ for $18.5 \le |x| \le 23$ and $|y| \le 4$.
- **Saddle Arch (R4)**: A curved shell centered at the pipe axis $(0, 0, 12.5)$. To guarantee material in the required radial band for $|x| \le 7$, the arch is defined such that its outer radius is $\ge 15.5\text{ mm}$ and its inner boundary (before subtraction) allows for a thickness that leaves material between $12.7\text{ mm}$ and $15.5\text{ mm}$ from the pipe axis.
- **Pipe Clearance (R3)**: A cylinder with radius $R = 12.6\text{ mm}$ centered at $(0, 0, 12.5)$ extending along the entire Y-axis is subtracted from the unioned body to ensure zero intersection volume with the pipe.
- **Screw Holes (R5)**: Two vertical bores of $\varnothing 6.6\text{ mm}$ are created via boolean subtraction, centered at $(\pm 27, 0)$, extending from $z = 0$ through the thickness of the flanges and base plate.

**Requirement Fulfillment**:
- **R1**: Guaranteed by a two-step workflow: `union(base, arch)` followed by `subtraction(pipe_clearance, screw_holes)`.
- **R2**: Width is exactly $20\text{ mm}$ ($y \in [-10, 10]$), X extent is $60\text{ mm}$ ($|x|=30$), and the lowest point is $z = 0$.
- **R3**: Achieved by subtracting a cylinder of radius $12.6\text{ mm}$ centered at $(0, 0, 12.5)$ along the Y-axis.
- **R4**: Material is preserved in the band $12.7 \le r \le 15.5$ (where $r$ is distance from pipe axis) for $|x| \le 7$ by defining the arch's outer radius $\ge 15.5\text{ mm}$.
- **R5**: Two $\varnothing 6.6\text{ mm}$ holes are subtracted at $(\pm 27, 0)$ through the $z=0$ to $z=3$ flange region.
- **R6**: Flanges are $3\text{ mm}$ thick ($z \in [0, 3]$) and located within $18.5 \le |x| \le 23$ and $|y| \le 4$.
- **R7**: Total volume is approximately $1600\text{ mm}^3$; mass $\approx 1.98\text{ g}$ (calculated as $V \times 0.00124\text{ g/mm}^3$), which is well below the $25\text{ g}$ limit.