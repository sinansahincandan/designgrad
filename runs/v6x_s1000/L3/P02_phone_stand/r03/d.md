**Concept**: A single-piece, continuous "ribbed spine" design. The structure consists of a Base Plate connected to a continuous structural rib that travels from the front lip/seat, through the phone's contact area, and up to the back support. This ensures R1 (single solid) is met while providing a rigid skeleton to counteract the phone's leaning moment.

**Main Features**:
- **Base Plate**: A flat plate with $x \in [-50, 40]$ and $y \in [-40, 40]$. The extension into negative $X$ ($-50$) is designed to counterbalance the phone's center of mass while staying within the $100\text{ mm}$ footprint limit. Thickness is $3\text{ mm}$.
- **Continuous Spine/Rib**: A structural element with a thickness of $4\text{ mm}$ that integrates all components via a single swept or lofted volume to ensure R1:
    - **Seat & Lip (R5)**: Defined relative to the phone's local coordinate system $(a, b, n)$ to avoid intersection (R3). 
        - **Seat**: Located at $a \in [-4, 0]$, $b \in [-8, 0]$ (offset in $-n$ direction to stay below/behind the bottom edge), and $|y| \le 15$.
        - **Lip**: Located at $a \in [0, 8]$, $b \in [1, 5]$ (offset in $-n$ direction to avoid intersection), and $|y| \le 15$.
    - **Back Support (R4)**: A vertical section positioned at the phone's leaning axis $\vec{u}$ at $a = 100$, spanning $b \in [-2, 0]$ and $|y| \le 15$. To satisfy R3, the rib thickness extends in the $-n$ direction (away from the phone volume).
- **Load Path**: Gravity $\to$ Phone $\to$ Lip/Seat $\to$ Continuous Spine $\to$ Base Plate $\to$ Desk.

**Requirement Fulfillment**:
- **R1 (Connectivity)**: All components (Base, Seat, Lip, Back Support) are modeled as a single union of primitives via the continuous spine.
- **R2 (Footprint & Height)**: Footprint is $90 \times 80\text{ mm}$ (within $100 \times 100$ limit). Max height $\approx 105\text{ mm}$ (within $120\text{ mm}$ limit). Min $z=0$.
- **R3 (No Intersection)**: Geometry is explicitly offset in the $-n$ direction for the Seat, Lip, and Back Support to ensure no overlap with the phone volume defined by $(a, b, n)$.
- **R4 (Back Support)**: Material placed at $a = 100$, $b \in [-2, 0]$, and $|y| \le 15$.
- **R5 (Seat & Lip)**: Seat occupies $a \in [-4, 0], b \in [-8, 0]$; Front lip occupies $a \in [0, 8], b \in [1, 5]$. Both within $|y| \le 15$.
- **R6 (Stability)**: The phone's COM is at approx $x = -32.7$. With the base plate extending to $x = -50$, the combined COM (Phone $200\text{g}$ + Stand $\approx 35\text{g}$) projects near $x \approx -31$. This provides a margin of $\approx 19\text{ mm}$ from the edge ($x=-50$), which is well above the required $5\text{ mm}$.
- **R7 (Mass)**: Using a $4\text{ mm}$ rib thickness and a $3\text{ mm}$ base plate, total volume is $\approx 28,000 \text{ mm}^3$. At $1.24 \text{ g/cm}^3$, mass $\approx 35\text{g}$, which is $<60\text{g}$.