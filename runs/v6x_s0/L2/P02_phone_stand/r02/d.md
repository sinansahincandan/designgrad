**Concept**: A lightweight, skeletal "hook-and-brace" stand consisting of a thin base plate with internal ribbing, a vertical web-like support structure, and contact volumes (Seat, Lip, and Rear Brace) that are transformed from the phone's local coordinate system to global space with an explicit clearance buffer.

**Main Features**:
- **Base Plate**: A thin $2\text{mm}$ thick plate with a footprint of $80\text{mm} \times 80\text{mm}$ (centered at $x=0, y=0$). The entire assembly must be constrained such that the minimum $z$ coordinate is exactly $0$.
- **Support Spine/Web**: A skeletal lattice or ultra-thin web structure ($<2\text{mm}$ thickness) that connects the Seat/Lip to the Rear Brace. This structure must be oriented vertically such that its maximum vertical extent ($z$) does not exceed $50\text{mm}$, and it must stay within the footprint of $x \in [-50, 50], y \in [-50, 50]$ to prevent X-axis violations.
- **Contact Volume Transformation Logic**: All contact geometries (Seat, Lip, Rear Brace) are defined in the phone's local $(a, b)$ space and must be mapped to global $(x, y, z)$ coordinates using: $\vec{P}_{global} = (0, 0, 8) + a\cdot\vec{u} + b\cdot\vec{n}$. To satisfy R3, all volumes must include an offset of $-0.6\text{mm}$ along the phone's normal vector $\vec{n}$ or surface normals to ensure zero intersection in global space.
- **Seat (Explicit Volume)**: A thin shell or hollowed volume defined by $a \in [-4, 0], b \in [0, 9], |y| \le 15$ in local coordinates, transformed and offset per the logic above to satisfy R3 and R5.
- **Lip (Explicit Volume)**: A thin shell or hollowed volume defined by $a \in [0, 8], b \in [9, 13], |y| \le 15$ in local coordinates, transformed and offset per the logic above to satisfy R3 and R5.
- **Rear Brace (Explicit Volume)**: A thin structural member placed at $a \in [90, 110]$ and $b \in [-2, 0], |y| \le 15$ in local coordinates, transformed and offset per the logic above to satisfy R3 and R4.

**Load Path**: The weight of the phone is transferred through the thin Seat and Lip into the skeletal Support Web; the web transfers the load via the Rear Brace and the main structural body into the ribbed Base Plate, which distributes the force to the desk.

**Requirement Fulfillment**:
- **R1**: All components (Base, Web, Seat, Lip, Brace) are combined using a single `union` operation to create one valid solid.
- **R2**: Footprint is $80\text{x}80\text{mm}$ (within $100\text{x}100$ limit); Max height $\le 50\text{mm}$; $z_{min} = 0$. The structure is contained within $x \in [-50, 50], y \in [-50, 50]$.
- **R3**: All contact geometries are transformed to global space and apply a $-0.6\text{mm}$ offset along the phone's normal $\vec{n}$ to ensure zero intersection.
- **R4**: Rear brace is explicitly placed within $a \in [90, 110]$ and $b \in [-2, 0]$ in local coordinates.
- **R5**: Seat ($a \in [-4, 0], b \in [0, 9]$) and Lip ($a \in [0, 8], b \in [9, 13]$) are defined as explicit volumes within the union.
- **R6**: The wide $80\text{mm}$ footprint and centered mass of the stand ensure the combined center of mass projects into the contact area with $>5\text{mm}$ margin.
- **R7**: By using a skeletal lattice spine, thin shells for contact volumes, and a ribbed base, the target volume is $\le 45,000 \text{ mm}^3$. At $1.24 \text{ g/cm}^3$, the mass is $\le 55.8\text{g}$, providing a safe margin below the $60\text{g}$ limit.