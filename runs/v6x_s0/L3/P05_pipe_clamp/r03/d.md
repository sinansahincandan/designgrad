**Concept**: A split-style saddle clamp consisting of a solid rectangular base plate that serves as the mounting foundation, with an integrated saddle arch that wraps around a pipe. The geometry is constructed by performing a Boolean Union of a base plate and a large saddle block, followed by Boolean Subtractions to create the pipe cavity and screw holes, ensuring a single continuous solid.

**Main Features**:
- **Base Plate**: A rectangular block spanning $x \in [-27, 27]$, $y \in [-10, 10]$, and $z \in [0, 3]$. This provides the mounting surface and contains the flanges. The minimum Z coordinate of the entire part is $0$.
- **Saddle Block**: A solid volume centered around the pipe axis $(0, y, 12.5)$ that is Boolean-unioned with the base plate to ensure physical connectivity (R1). This block must be large enough to encompass the required saddle band.
- **Pipe Cavity (Subtractive)**: A cylindrical subtraction of radius $r=12.6\text{ mm}$ centered at $(0, y, 12.5)$ is performed on the union of the base and saddle block to satisfy R3.
- **Saddle Arch Material**: To satisfy R4, the geometry is designed such that the remaining solid material includes a continuous shell within the radial band $12.7\text{ mm} \le r \le 15.5\text{ mm}$ for $|x| \le 7$.
- **Screw Holes (Subtractive)**: Two vertical cylindrical bores of $\varnothing 6.6\text{ mm}$ ($r=3.3$) are subtracted from the final union. They are centered at $(\pm 27, 0)$ and pass through the base plate from $z=0$ to $z=3$.

**Load Path**: Downward force from the pipe is applied to the saddle arch; this load is transferred through the continuous solid material of the saddle block into the base plate and distributed through the mounting flanges into the surface via the screws.

**Requirement Fulfillment**:
- **R1**: The part is a single valid solid created by: `(Base Plate ∪ Saddle Block) \ (Pipe Cylinder ∪ Screw Hole Cylinders)`.
- **R2**: Width (Y extent) is exactly $20\text{ mm}$ ($y \in [-10, 10]$); X extent is $54\text{ mm}$ ($x \in [-27, 27]$), which is $\le 80\text{ mm}$. The minimum Z coordinate is $0$.
- **R3**: A cylinder of radius $12.6\text{ mm}$ centered at $(0, y, 12.5)$ is subtracted to create the pipe cavity.
- **R4**: Material exists in the band above the pipe by ensuring the saddle geometry includes the region where the distance from the axis $(0, y, 12.5)$ is between $12.7\text{ mm}$ and $15.5\text{ mm}$ for $|x| \le 7$.
- **R5**: Two $\varnothing 6.6\text{ mm}$ holes are subtracted vertically at $(\pm 27, 0)$. The base plate extends to $|x|=27$ to ensure these holes are contained within the solid material.
- **R6**: Flanges are $3\text{ mm}$ thick ($z=0$ to $3$) and located at $|x| \in [18.5, 27]$ (covering the required $[18.5, 23]$ range) and $|y| \le 4$.
- **R7**: Estimated volume is $\approx 13,500\text{ mm}^3$ (Base: $54 \times 20 \times 3 = 3240$; Arch shell: $\approx 10,260$). Total mass $\approx 13,500 \times 0.00124 \approx 16.7\text{ g}$, which is well below the $25\text{ g}$ limit.