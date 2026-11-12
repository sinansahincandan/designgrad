**Concept**: A lightweight, hollowed "hook-and-brace" style stand consisting of a thin base plate with internal ribbing, a thin-walled hollow I-beam support spine, and explicit contact volumes (Seat, Lip, and Rear Brace) designed using subtraction logic to ensure zero intersection with the phone.

**Main Features**:
- **Base Plate**: A $2\text{mm}$ thick plate ($z \in [0, 2]$) with a footprint of $95\text{mm} \times 80\text{mm}$ (centered at $x=0, y=0$) to ensure stability and compliance with R2. The bottom surface is explicitly set at $z=0$.
- **Support Spine**: A thin-walled hollow I-beam structure (wall thickness $\le 1.5\text{mm}$) following the phone's tilt ($65^\circ$). To satisfy R2, the spine's vertical extent is strictly capped at $z_{max} = 110\text{mm}$.
- **Seat (Explicit Volume)**: A structural block defined by $a \in [-4, 0], b \in [0, 9], |y| \le 15$. To satisfy R3, this volume is defined as the intersection of a solid shape and the complement of (Phone Volume + $0.5\text{mm}$ offset).
- **Lip (Explicit Volume)**: A structural block defined by $a \in [0, 8], b \in [9, 13], |y| \le 15$. To satisfy R3, this volume is defined as the intersection of a solid shape and the complement of (Phone Volume + $0.5\text{mm}$ offset).
- **Rear Brace (Explicit Volume)**: A structural member placed at $a \in [90, 110]$ and $b \in [-2, 0], |y| \le 15$. To satisfy R3, this volume is defined as the intersection of a solid shape and the complement of (Phone Volume + $0.5\text{mm}$ offset). The base plate is extended to ensure this brace remains within the $x \in [-50, 50]$ footprint.

**Load Path**: The weight of the phone is transferred through the Seat and Lip into the thin-walled Support Spine; the spine transfers the load via the Rear Brace and the main structural body into the ribbed Base Plate, which distributes the force to the desk.

**Requirement Fulfillment**:
- **R1**: All components (Base, Spine, Seat, Lip, Brace) are combined using a single `union` operation to create one valid solid.
- **R2**: Footprint is within $100\text{x}100\text{mm}$ (max width $\approx 95\text{mm}$); Max height is capped at $110\text{mm}$; $z_{min} = 0$.
- **R3**: All contact geometries are defined by subtracting the phone's mathematical volume plus a $0.5\text{mm}$ Minkowski sum/offset from the intended structural shapes to guarantee zero intersection.
- **R4**: Rear brace is explicitly placed within $a \in [90, 110]$ and $b \in [-2, 0]$.
- **R5**: Seat ($a \in [-4, 0], b \in [0, 9]$) and Lip ($a \in [0, 8], b \in [9, 13]$) are defined as explicit volumes within the union.
- **R6**: The $95\text{mm}$ wide footprint and centered mass of the stand ensure the combined center of mass projects into the contact area with $>5\text{mm}$ margin.
- **R7**: By using a thin-walled hollow I-beam spine ($\le 1.5\text{mm}$) and a $2\text{mm}$ ribbed base, the target volume is $\approx 35,000 \text{ mm}^3$. At $1.24 \text{ g/cm}^3$, the mass is $\approx 43.4\text{g}$, providing a safe margin below the $60\text{g}$ limit.