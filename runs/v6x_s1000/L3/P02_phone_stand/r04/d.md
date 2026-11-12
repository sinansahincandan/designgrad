**Concept**: A single-piece, continuous "ribbed spine" design. The structure consists of a Base Plate connected to a thin structural rib that travels from the front lip/seat, through the phone's contact area, and up to the back support. This ensures R1 (single solid) is met while providing a rigid skeleton to counteract the phone's leaning moment.

**Coordinate Transformation**:
To ensure R3 (No Intersection) and correct placement of features, all local phone coordinates $(a, b)$ are mapped to global $(x, z)$ using:
$P_{global} = (0, y, 8) + a \cdot \vec{u} + b \cdot \vec{n}$
where $\vec{u} = (-\cos 65^\circ, 0, \sin 65^\circ)$ and $\vec{n} = (\sin 65^\circ, 0, \cos 65^\circ)$.

**Main Features**:
- **Base Plate**: A flat plate with $x \in [-50, 40]$ and $y \in [-40, 40]$. Thickness is $3\text{ mm}$. The extension to $x = -50$ provides the necessary counterbalance for stability (R6).
- **Continuous Spine/Rib**: A thin swept profile with a thickness of $4\text{ mm}$ to ensure mass remains well below the limit (R7). It connects the Base Plate, Seat, Lip, and Back Support into one solid (R1).
    - **Seat (R5)**: Located at $a \in [-4, 0]$ and $b \in [0, 9]$. To satisfy R3 (No Intersection), the rib is placed at a small negative offset in the $\vec{n}$ direction relative to these bounds. $|y| \le 15$.
    - **Lip (R5)**: Located at $a \in [0, 8]$ and $b \in [9, 13]$. To satisfy R3, the rib is placed at a small negative offset in the $\vec{n}$ direction. $|y| \le 15$.
    - **Back Support (R4)**: Positioned at the phone's leaning axis $\vec{u}$ at $a = 100$, spanning $b \in [-2, 0]$ and $|y| \le 15$. To satisfy R3, the rib thickness extends in the $-n$ direction (away from the phone volume).
- **Load Path**: Gravity $\to$ Phone $\to$ Lip/Seat $\to$ Continuous Spine $\to$ Base Plate $\to$ Desk.

**Requirement Fulfillment**:
- **R1 (Connectivity)**: All components are modeled as a single union of primitives via a thin, swept continuous spine.
- **R2 (Footprint & Height)**: Footprint is $90 \times 80\text{ mm}$ ($x$ from $-50$ to $40$, $y$ from $-40$ to $40$). Max height at $a=100$ is approximately $z = 8 + 100\sin(65^\circ) \approx 98.7\text{ mm}$, which is within the $120\text{ mm}$ limit.
- **R3 (No Intersection)**: All contact features (Seat, Lip, Back Support) are explicitly offset in the $-\vec{n}$ direction to ensure no overlap with the phone volume defined by $(a, b, n)$.
- **R4 (Back Support)**: Material is placed at $a = 100$, $b \in [-2, 0]$, and $|y| \le 15$.
- **R5 (Seat & Lip)**: Seat occupies $a \in [-4, 0], b \in [0, 9]$; Front lip occupies $a \in [0, 8], b \in [9, 13]$. Both within $|y| \le 15$.
- **R6 (Stability)**: The phone's COM is at approx $x = -32.7$. With the base plate extending to $x = -50$, the combined COM (Phone $200\text{g}$ + Stand $\approx 35\text{g}$) projects near $x \approx -31$. This provides a margin of $\approx 19\text{ mm}$ from the edge ($x=-50$), exceeding the required $5\text{ mm}$.
- **R7 (Mass)**: By using a thin swept profile ($4\text{ mm}$) for the spine and a $3\text{ mm}$ base plate, total volume is $\approx 28,000 \text{ mm}^3$. At $1.24 \text{ g/cm}^3$, mass $\approx 35\text{g}$, which is well below the $60\text{g}$ limit.