**Concept**: A lightweight, skeletal "hook-and-brace" stand designed as a single continuous solid. It utilizes a thin base plate and a slimmed-down support spine to provide stability while strictly adhering to the phone's geometry without intersection through explicit boolean subtraction.

**Main Features**:
- **Base Plate**: A flat plate centered at $x=0, y=0$ with thickness 2mm, lying on the plane $z=0$. Footprint is constrained to $x \in [-50, 50]$ and $y \in [-50, 50]$ to ensure it stays within the 100x100mm limit (R2).
- **Support Spine**: A slimmed-down structural member (thickness $\approx$ 2.5–3mm) that follows the phone's tilt. To prevent interference (R3), the spine is defined as a primitive volume and then processed via `Result = (Base + Spine + Seat + Lip + Brace) - V_phone`.
- **Seat**: A dedicated volume integrated into the single solid, occupying $a \in [-4, 0], b \in [0, 9], |y| \le 15$ to cradle the bottom edge (R5). This volume is also subject to boolean subtraction from $V_{phone}$ to ensure zero intersection.
- **Lip**: A front protrusion integrated into the single solid, occupying $a \in [0, 8], b \in [9, 13], |y| \le 15$ to prevent forward sliding (R5). This volume is also subject to boolean subtraction from $V_{phone}$ to ensure zero intersection.
- **Rear Brace**: A vertical/angled support located behind the phone at $a \in [70, 90]$ and $b \in [-2, 0]$, near the mid-section $|y| \le 15$ (R4). The range of $a$ is adjusted to ensure that even with the phone's tilt ($u = -\cos65^\circ$), the resulting $x$-coordinates remain within the $[-50, 50]$ footprint limit.

**Load Path**: The weight of the phone is transferred from the seat and lip into the support spine. The spine directs this load through the rear brace and down to the base plate, which distributes the force across the desk surface ($z=0$).

**Requirement Fulfillment**:
- **R1 (Single Solid)**: All components are joined via a single boolean union operation, followed by a final boolean subtraction of the phone volume $V_{phone}$ to ensure no intersections.
- **R2 (Dimensions)**: Base is on $z=0$. Footprint is strictly within $[-50, 50]$ for both $x$ and $y$. Max height is kept below 120mm.
- **R3 (No Interference)**: Geometry is explicitly defined using the logic `Result = (Base + Spine + Seat + Lip + Brace) - V_phone` to guarantee no intersection with the phone volume.
- **R4 (Back Support)**: Material placed at $a \in [70, 90], b \in [-2, 0], |y| \le 15$. The $a$ range is optimized to keep $|x| \le 50$.
- **R5 (Seat & Lip)**: Seat defined at $a \in [-4, 0], b \in [0, 9]$; Lip defined at $a \in [0, 8], b \in [9, 13]$. Both within $|y| \le 15$.
- **R6 (Stability)**: The base is centered at $x=0$ with a width of 90mm ($y \in [-45, 45]$). This wide footprint ensures the combined center of mass projects into the contact area with a $>5\text{mm}$ margin.
- **R7 (Mass)**: To ensure compliance with the 60g limit, the base thickness is reduced to 2mm and spine thickness to 2.5–3mm. Total target volume is $< 45,000 \text{ mm}^3$ ($\approx 55\text{g}$), providing a safe buffer below the $60\text{g}$ limit.