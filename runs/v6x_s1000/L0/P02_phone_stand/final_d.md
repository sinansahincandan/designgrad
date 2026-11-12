**Concept**: A minimalist "L-shaped" bracket design with a reinforced back support and a front lip to cradle the phone's bottom edge. The stand uses a wide base to ensure stability against the leaning moment of the phone.

**Main Features**:
- **Base Plate**: Extends from $x = -40$ to $x = 20$ and $y = -45$ to $y = 45$ to provide a large footprint for stability.
- **Back Support**: A vertical strut located near the phone's mid-section ($a \approx 100$) to prevent the phone from tipping backward.
- **Cradle/Lip**: A small protrusion at the bottom edge $(a=0)$ that catches both the bottom face and the front lip of the phone.
- **Load Path**: Gravity $\to$ Phone $\to$ Lip/Back Support $\to$ Base Plate $\to$ Desk.

**Requirement Fulfillment**:
- R1: Created using a single union of primitives (base, upright, supports).
- R2: Footprint is $60 \times 90$ mm; Height is approx $50$ mm; Min $z=0$.
- R3: Geometry is offset from the phone's mathematical volume.
- R4: Back support placed at $a=100, |y| \le 15$, within $2$ mm of the back face.
- R5: Lip and seat geometry designed to intercept the phone at $a \in [-4, 8]$.
- R6: Wide base ($x$ range $-40$ to $20$) ensures the COM (centered near $x=-10$) projects well within the footprint with $>5$ mm margin.
- R7: Total volume is approx $35,000 \text{ mm}^3$, mass $\approx 43\text{g}$ ($<60\text{g}$).