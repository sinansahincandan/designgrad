**Concept**: A lightweight, skeletal "hook-and-brace" stand designed as a single continuous solid. It utilizes a thin base plate and a structural spine that follows the phone's tilt. To ensure zero interference and strict adherence to footprint constraints, the geometry is defined by constructing an intended support volume and then performing a boolean subtraction of the phone's volume.

**Main Features**:
- **Base Plate**: A flat plate centered at $x=0, y=0$ with thickness 3mm, lying on the plane $z=0$. The footprint is strictly constrained to ensure $\max(x) - \min(x) \le 100$ and $\max(y) - \min(y) \le 100$ (R2).
- **Support Spine**: A structural member that provides the connection between all components. To guarantee zero intersection with the phone (R3), the spine is constructed as: `Spine = (Intended_Spine_Volume) - V_phone`. The intended volume follows a path from the Seat, through the Rear Brace zone, down to the Base Plate.
- **Seat**: A dedicated volume integrated into the single solid, occupying $a \in [-4, 0], b \in [0, 9], |y| \le 15$ to cradle the bottom edge (R5).
- **Lip**: A front protrusion integrated into the single solid, occupying $a \in [0, 8], b \in [9, 13], |y| \le 15$ to prevent forward sliding (R5).
- **Rear Brace**: A vertical/angled support located behind the phone. To satisfy R4 and stay within the footprint (R2), the brace is placed at $a \in [90, 110]$ and $b \in [-2, 0]$, near $|y| \le 15$. The $a$-coordinates are chosen such that the resulting $x$ coordinates (calculated via $x = -a \cdot \cos(65^\circ)$) do not cause the total $x$-span of the part to exceed 100mm.

**Load Path**: The weight of the phone is transferred from the seat and lip into the support spine. The spine acts as a continuous manifold, directing this load through the rear brace (ensuring material presence at the required $a$ range) and down to the base plate, which distributes the force across the desk surface ($z=0$).

**Requirement Fulfillment**:
- **R1 (Single Solid)**: All components (Base, Spine, Seat, Lip, Brace) are joined via a single boolean union operation.
- **R2 (Dimensions)**: Base is on $z=0$. The total bounding box for all components is explicitly checked to ensure $\Delta x \le 100$ and $\Delta y \le 100$, with max height $< 120\text{mm}$.
- **R3 (No Interference)**: Guaranteed by defining the spine as `(Intended_Spine_Volume) - V_phone`.
- **R4 (Back Support)**: The spine is a continuous manifold that explicitly intersects the region $a \in [90, 110], b \in [-2, 0], |y| \le 15$.
- **R5 (Seat & Lip)**: Seat defined at $a \in [-4, 0], b \in [0, 9]$; Lip defined at $a \in [0, 8], b \in [9, 13]$. Both within $|y| \le 15$.
- **R6 (Stability)**: The base is centered and sized to ensure the combined center of mass (stand + phone) projects into the contact area with a $>5\text{mm}$ margin.
- **R7 (Mass)**: Total target volume is kept $< 48,000 \text{ mm}^3$ ($\approx 59\text{g}$) by using thin-walled sections (3–5mm) for the spine and base to stay under the $60\text{g}$ limit.