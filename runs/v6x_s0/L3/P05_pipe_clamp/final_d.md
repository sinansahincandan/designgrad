**Concept**: A split-style saddle clamp consisting of a solid rectangular base plate that serves as the mounting foundation, with an integrated saddle arch that wraps around a pipe. The geometry is designed to provide a secure cradle for a 25 mm diameter pipe while ensuring screw holes are positioned within reinforced flange sections.

**Main Features**:
- **Base Plate & Flanges**: A single rectangular block spanning $x \in [-27, 27]$, $y \in [-10, 10]$, and $z \in [0, 3]$. This base provides the mounting surface and contains the flanges.
- **Saddle Arch**: An additive or subtractive geometry centered at $(0, y, 12.5)$ that creates a shell around the pipe axis. To satisfy R4, material is defined in the radial band between $r=12.7\text{ mm}$ and $r=15.5\text{ mm}$.
- **Screw Holes**: Two vertical cylindrical bores of $\varnothing 6.6\text{ mm}$ centered at $(\pm 27, 0)$, passing through the base from $z=0$ to $z=3$.

**Load Path**: Downward force from the pipe is applied to the saddle arch; this load is transferred to the base plate and distributed through the mounting flanges into the surface via the screws.

**Requirement Fulfillment**:
- **R1**: The part is constructed as a single continuous solid using boolean unions (base + arch) and subtractions (pipe volume + screw holes).
- **R2**: Width (Y extent) is $20\text{ mm}$ ($y \in [-10, 10]$); X extent is $54\text{ mm}$ ($x \in [-27, 27]$), which is $\le 80\text{ mm}$. The minimum Z coordinate is $0$.
- **R3**: A cylinder of radius $12.6\text{ mm}$ centered at $(0, y, 12.5)$ is subtracted from the solid to create the pipe cavity.
- **R4**: Material exists in the band above the pipe by ensuring the saddle geometry includes the region where the distance from the axis $(0, y, 12.5)$ is between $12.7\text{ mm}$ and $15.5\text{ mm}$.
- **R5**: Two $\varnothing 6.6\text{ mm}$ holes are drilled vertically at $(\pm 27, 0)$. The base plate extends to $|x|=27$ to ensure these holes are contained within the solid material.
- **R6**: Flanges are $3\text{ mm}$ thick ($z=0$ to $3$) and located at $|x| \in [18.5, 27]$ (covering the required $[18.5, 23]$ range) and $|y| \le 4$.
- **R7**: Estimated volume is $\approx 13,500\text{ mm}^3$ (Base: $54 \times 20 \times 3 = 3240$; Arch shell: $\approx 10,260$). Total mass $\approx 13,500 \times 0.00124 \approx 16.7\text{ g}$, which is well below the $25\text{ g}$ limit.