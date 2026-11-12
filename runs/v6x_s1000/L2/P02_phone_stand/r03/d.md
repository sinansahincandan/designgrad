**Concept**: A minimalist "L-shaped" bracket design featuring a wide, stable base plate, a precisely positioned back support to prevent backward tipping, and a dual-component cradle (seat and lip) to secure the phone's bottom edge. The geometry is specifically offset from the phone's tilted volume to ensure zero intersection.

**Main Features**:
- **Base Plate**: Extends from $x = -40$ to $x = 20$ and $y = -45$ to $y = 45$ to provide a large footprint for stability.
- **Back Support**: A vertical plate located at $a \in [90, 110]$, spanning $|y| \le 15$, with thickness occupying the region $b \in [-2, 0]$ (directly behind the phone's back face).
- **Cradle/Lip System**:
    - **Seat**: A horizontal surface covering $a \in [-4, 0]$ and $b \in [0, 9]$ for $|y| \le 15$, supporting the bottom edge.
    - **Lip**: A vertical protrusion at the front edge covering $a \in [0, 8]$ and $b \in [9, 13]$ for $|y| \le 15$, preventing forward sliding.
- **Load Path**: Gravity $\to$ Phone $\to$ Lip/Seat/Back Support $\to$ Base Plate $\to$ Desk.

**Requirement Fulfillment**:
- R1: Created using a single union of primitives (base, uprights, seat, lip, and back support).
- R2: Footprint is $60 \times 90$ mm; Height is approx $50$ mm; Min $z=0$.
- R3: Geometry is explicitly offset from the phone's mathematical volume by placing material in the specified $b$ ranges (e.g., $b \in [-2, 0]$ for back support).
- R4: Back support placed at $a \in [90, 110], |y| \le 15$, within the required $2$ mm of the back face ($b \in [-2, 0]$).
- R5: Seat ($a \in [-4, 0], b \in [0, 9]$) and Lip ($a \in [0, 8], b \in [9, 13]$) geometry designed to intercept the phone at $|y| \le 15$.
- R6: Wide base ($x$ range $-40$ to $20$) ensures the combined COM (centered near $x=-10$) projects well within the footprint with $>5$ mm margin.
- R7: Total volume is approx $35,000 \text{ mm}^3$, mass $\approx 43\text{g}$ ($<60\text{g}$).