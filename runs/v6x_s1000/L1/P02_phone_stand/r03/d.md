**Concept**: A minimalist "L-shaped" bracket design with a reinforced back support and a front lip to cradle the phone's bottom edge. The stand uses a wide, continuous base plate to connect the front cradle to the distant back support, ensuring structural integrity (R1) and stability against the leaning moment of the phone.

**Main Features**:
- **Base Plate**: A thick, continuous slab extending from $x = -50$ to $x = 20$ and $y = -45$ to $y = 45$. This provides a large footprint for stability and serves as the structural foundation connecting all components.
- **Back Support**: A vertical strut located at the phone's back position ($a=100$). At this point, the phone is at $x \approx -42.3$ and $z \approx 98.3$. The support is a block spanning $x \in [-44, -42]$, $y \in [-15, 15]$, and $z \in [0, 100]$ to provide contact within the required $b \in [-2, 0]$ range.
- **Cradle/Lip**: Two distinct geometric primitives integrated into the base:
    - **Seat**: A block at $a \in [-4, 0], b \in [-2, 0]$, located approximately at $x \in [-5, 0], z \in [0, 8]$.
    - **Lip**: A protrusion at $a \in [0, 8], b \in [9, 13]$, located approximately at $x \in [0, 2], z \in [0, 15]$.
- **Load Path**: Gravity $\to$ Phone $\to$ Lip/Seat & Back Support $\to$ Continuous Base Plate $\to$ Desk.

**Requirement Fulfillment**:
- R1: Created using a single union of primitives (base plate, back strut, seat, and lip).
- R2: Footprint is $70 \times 90$ mm; Height is approx $100$ mm; Min $z=0$.
- R3: Geometry is offset from the phone's mathematical volume by placing supports at specific $x, z$ coordinates calculated from the phone's lean angle.
- R4: Back support placed at $a=100$, which corresponds to $x \approx -42$, satisfying the $b \in [-2, 0]$ requirement and avoiding intersection with the phone's volume.
- R5: Seat defined for $a \in [-4, 0], b \in [-2, 0]$ and Lip defined for $a \in [0, 8], b \in [9, 13]$ to prevent sliding.
- R6: Wide base ($x$ range $-50$ to $20$) ensures the combined COM (phone + stand) projects well within the footprint with $>5$ mm margin.
- R7: Total volume is approx $32,000 \text{ mm}^3$, mass $\approx 39.7\text{g}$ ($<60\text{g}$).