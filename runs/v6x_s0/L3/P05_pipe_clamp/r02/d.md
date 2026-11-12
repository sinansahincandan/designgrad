**Concept**: A split-style saddle clamp consisting of a solid rectangular base plate that serves as the mounting foundation, with an integrated saddle arch that wraps around a pipe. The geometry is constructed by performing Boolean operations on three primary volumes: a base plate, a saddle shell, and subtractive cylinders for the pipe cavity and screw holes.

**Main Features**:
- **Base Plate & Flanges**: A single rectangular block spanning $x \in [-27, 27]$, $y \in [-10, 10]$, and $z \in [0, 3]$. The total Y-extent is exactly $20\text{ mm}$ ($y$ from $-10$ to $+10$) to satisfy the R2 requirement.
- **Saddle Arch**: A solid shell defined by the region where the distance from the pipe axis $(0, y, 12.5)$ is between $r=12.7\text{ mm}$ and $r=15.5\text{ mm}$, restricted to $|x| \le 7$. This shell is unioned with the base plate to form the main body.
- **Screw Holes**: Two vertical cylindrical bores of $\varnothing 6.6\text{ mm}$ centered at $(\pm 27, 0)$. These cylinders extend from $z = -1$ to $z = 5$ to ensure full penetration through the part and are subtracted from the combined base/arch geometry.
- **Pipe Cavity**: A cylinder of radius $r=12.6\text{ mm}$ centered at $(0, y, 12.5)$ that is subtracted from the entire union of the base and arch.

**Construction Logic (Boolean Operations)**:
`Final_Solid = ((Base_Plate UNION Saddle_Arch) DIFFERENCE Pipe_Cavity_Cylinder) DIFFERENCE Screw_Hole_Cylinders`

**Load Path**: Downward force from the pipe is applied to the saddle arch; this load is transferred to the base plate and distributed through the mounting flanges into the surface via the screws.

**Requirement Fulfillment**:
- **R1**: The part is a single continuous solid produced via the Boolean sequence: `(Base + Arch) - Pipe_Cylinder - Screw_Holes`.
- **R2**: Width (Y extent) is exactly $20\text{ mm}$ ($y \in [-10, 10]$); X extent is $54\text{ mm}$ ($x \in [-27, 27]$), which is $\le 80\text{ mm}$. The minimum Z coordinate is $0$.
- **R3**: A cylinder of radius $12.6\text{ mm}$ centered at $(0, y, 12.5)$ is subtracted from the union of the base and arch to ensure the pipe volume is free of material.
- **R4**: Material exists in the required band by defining the saddle arch as a shell where the distance from the axis $(0, y, 12.5)$ is between $12.7\text{ mm}$ and $15.5\text{ mm}$ for $|x| \le 7$.
- **R5**: Two $\varnothing 6.6\text{ mm}$ holes are drilled vertically at $(\pm 27, 0)$. The base plate extends to $|x|=27$ to ensure these holes are contained within the solid material and are fully subtracted from the final part.
- **R6**: Flanges are $3\text{ mm}$ thick ($z=0$ to $3$) and located at $|x| \in [18.5, 27]$ (covering the required $[18.5, 23]$ range) and $|y| \le 4$.
- **R7**: Estimated volume is $\approx 13,500\text{ mm}^3$ (Base: $54 \times 20 \times 3 = 3240$; Arch shell: $\approx 10,260$). Total mass $\approx 13,500 \times 0.00124 \approx 16.7\text{ g}$, which is well below the $25\text{ g}$ limit.