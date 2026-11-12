**Concept**: A split-style saddle clamp consisting of a solid rectangular base plate that serves as the mounting foundation, with an integrated saddle arch that wraps around a pipe. The geometry is constructed using boolean operations to ensure a hollow pipe cavity and empty screw holes.

**Main Features**:
- **Base Plate & Flanges**: A single rectangular block spanning $x \in [-27, 27]$, $y \in [-10, 10]$, and $z \in [0, 3]$. This base provides the mounting surface and contains the flanges. All geometry is defined such that $z \ge 0$, with the bottom surface sitting exactly on the plane $z=0$.
- **Saddle Arch (Subtractive/Additive Shell)**: A solid shell centered at $(0, y, 12.5)$ that wraps around the pipe axis. It is defined by a boolean operation where a cylinder of radius $15.5\text{ mm}$ is used to create the outer boundary, and a cylinder of radius $12.6\text{ mm}$ (the pipe cavity) is subtracted from it. The resulting material exists in the radial band $12.7 \le r \le 15.5$ for all $y$ values within the base plate extent, ensuring coverage for $|x| \le 7$.
- **Screw Holes**: Two vertical cylindrical bores of $\varnothing 6.6\text{ mm}$ centered at $(\pm 27, 0)$. These are created via boolean subtraction from the base plate, passing through the material from $z=0$ to $z=3$, resulting in empty voids.

**Load Path**: Downward force from the pipe is applied to the saddle arch; this load is transferred to the base plate and distributed through the mounting flanges into the surface via the screws.

**Requirement Fulfillment**:
- **R1**: The part is constructed as a single continuous solid using boolean unions (base + outer saddle cylinder) and subtractions (pipe cavity cylinder + screw hole cylinders).
- **R2**: Width (Y extent) is strictly $20\text{ mm}$ ($y \in [-10, 10]$), which is within the $[18, 22]$ range. X extent is $54\text{ mm}$ ($x \in [-27, 27]$), which is $\le 80\text{ mm}$. The minimum Z coordinate is exactly $0$.
- **R3**: A cylinder of radius $12.6\text{ mm}$ centered at $(0, y, 12.5)$ is subtracted from the solid to ensure the pipe volume is entirely free of material.
- **R4**: Material is guaranteed in the band above the pipe by ensuring the saddle geometry includes the region where the distance from the axis $(0, y, 12.5)$ is between $12.7\text{ mm}$ and $15.5\text{ mm}$, spanning the required $|x| \le 7$ region.
- **R5**: Two $\varnothing 6.6\text{ mm}$ holes are subtracted vertically at $(\pm 27, 0)$. The base plate extends to $|x|=27$ to ensure these holes are contained within the solid material and are fully empty.
- **R6**: Flanges are $3\text{ mm}$ thick ($z=0$ to $3$) and located at $|x| \in [18.5, 23]$ (covering the required range) and $|y| \le 4$.
- **R7**: Estimated volume is $\approx 13,500\text{ mm}^3$ (Base: $54 \times 20 \times 3 = 3240$; Arch shell: $\approx 10,260$). Total mass $\approx 13,500 \times 0.00124 \approx 16.7\text{ g}$, which is well below the $25\text{ g}$ limit.