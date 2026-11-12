**Concept**: A minimalist "L-shaped" bracket design with a reinforced back support and a two-part cradle (seat and lip) to secure the phone's bottom edge. The stand uses a wide, thin base plate to ensure stability against the leaning moment of the phone while staying under the mass limit.

**Main Features**:
- **Base Plate**: Extends from $x = -40$ to $x = 20$ and $y = -45$ to $y = 45$ with a thickness of $3\text{ mm}$ to provide a stable footprint while minimizing mass.
- **Back Support**: A vertical strut located at $a \approx 100, |y| \le 15$. To satisfy R4 and avoid intersection (R3), the support is positioned at $x \in [-2, 0]$ to sit behind the tilted back face ($b \in [-2, 0]$).
- **Cradle/Lip**: A two-part feature designed to intercept the phone's thickness:
    1. **Seat**: Occupies $a \in [-4, 0], b \in [-2, 9], |y| \le 15$ to support the bottom edge.
    2. **Front Lip**: Occupies $a \in [0, 8], b \in [9, 13], |y| \le 15$ to prevent forward sliding.
- **Load Path**: Gravity $\to$ Phone $\to$ Seat/Lip & Back Support $\to$ Base Plate $\to$ Desk.

**Requirement Fulfillment**:
- R1: Created using a single union of primitives (base, upright, supports).
- R2: Footprint is $60 \times 90$ mm; Height is approx $110$ mm; Min $z=0$.
- R3: Geometry is offset from the phone's mathematical volume by placing the back support at negative $x$ values relative to the tilted face.
- R4: Back support placed at $a=100, |y| \le 15$, with $x$-coordinates adjusted to $x \in [-2, 0]$ to ensure it sits behind the tilted back face without intersecting the phone volume.
- R5: Seat ($a \in [-4, 0], b \in [-2, 9]$) and Lip ($a \in [0, 8], b \in [9, 13]$) geometry designed to match specification exactly.
- R6: Wide base ($x$ range $-40$ to $20$) ensures the combined COM (stand + phone) projects well within the footprint with $>5$ mm margin.
- R7: Total volume is targeted at $\approx 36,000 \text{ mm}^3$, resulting in a mass of $\approx 44.6\text{g}$ ($<60\text{g}$).