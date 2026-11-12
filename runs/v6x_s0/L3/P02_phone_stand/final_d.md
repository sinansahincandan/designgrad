**Concept**: A lightweight, skeletal "hook-and-brace" stand designed as a single continuous solid. It utilizes a thin base plate and a slimmed-down support spine to provide stability while strictly adhering to the phone's geometry without intersection.

**Main Features**:
- **Base Plate**: A flat plate centered at $x=0, y=0$ with thickness 3mm, lying on the plane $z=0$. Footprint is constrained to $x \in [-45, 45]$ and $y \in [-45, 45]$ to ensure it stays within the 100x100mm limit (R2).
- **Support Spine**: A slimmed-down structural member (thickness $\approx$ 4mm) that follows the phone's tilt. To prevent interference (R3), the spine is constructed by offsetting from the phone's volume or using boolean subtraction to ensure it only exists in the $b \in [-2, 0]$ region for the brace and the specific seat/lip regions.
- **Seat**: A dedicated volume integrated into the single solid, occupying $a \in [-4, 0], b \in [0, 9], |y| \le 15$ to cradle the bottom edge (R5).
- **Lip**: A front protrusion integrated into the single solid, occupying $a \in [0, 8], b \in [9, 13], |y| \le 15$ to prevent forward sliding (R5).
- **Rear Brace**: A vertical/angled support located behind the phone at $a \in [90, 110]$ and $b \in [-2, 0]$, near the mid-section $|y| \le 15$ (R4).

**Load Path**: The weight of the phone is transferred from the seat and lip into the support spine. The spine directs this load through the rear brace and down to the base plate, which distributes the force across the desk surface ($z=0$).

**Requirement Fulfillment**:
- **R1 (Single Solid)**: All components (Base, Spine, Seat, Lip, Brace) are joined via a single boolean union operation.
- **R2 (Dimensions)**: Base is on $z=0$. Footprint is within $[-50, 50]$ for both $x$ and $y$. Max height is kept below 120mm.
- **R3 (No Interference)**: Geometry is explicitly defined to exist only in the "behind" ($b \le 0$) or "lip" ($b \ge 9$) zones, or via boolean subtraction from the phone's volume $V_{phone}$.
- **R4 (Back Support)**: Material placed at $a \in [90, 110], b \in [-2, 0], |y| \le 15$.
- **R5 (Seat & Lip)**: Seat defined at $a \in [-4, 0], b \in [0, 9]$; Lip defined at $a \in [0, 8], b \in [9, 13]$. Both within $|y| \le 15$.
- **R6 (Stability)**: The base is centered at $x=0$ with a width of 90mm ($y \in [-45, 45]$). This wide footprint ensures the combined center of mass projects into the contact area with a $>5\text{mm}$ margin.
- **R7 (Mass)**: To prevent overshooting the 60g limit, the spine and base are designed with a maximum thickness of 3–5mm. Total target volume is $< 48,000 \text{ mm}^3$ ($\approx 59\text{g}$), providing a safety buffer below the $60\text{g}$ limit.