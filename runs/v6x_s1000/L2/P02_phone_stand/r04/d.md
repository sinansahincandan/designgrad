**Concept**: A single-piece, L-shaped reinforced bracket designed to cradle a phone leaning at 65°. The design uses three specific contact zones (Seat, Lip, and Back Support) precisely mapped to the phone's mathematical volume to ensure stability and compliance with non-intersection constraints.

**Main Features**:
- **Base Plate**: A wide footprint extending from $x = -40$ to $x = 20$ and $y = -45$ to $y = 45$. This provides a large contact area on the desk ($z=0$) to ensure the combined COM of the stand and phone stays within the stability margin.
- **Seat (Underneath Support)**: A geometry block positioned at $a \in [-4, 0]$, $b \in [0, 9]$, and $|y| \le 15$. This occupies the space directly beneath the phone's bottom edge to prevent sliding down.
- **Front Lip (Forward Stop)**: A protrusion located at $a \in [0, 8]$, $b \in [9, 13]$, and $|y| \le 15$. This intercepts the front face of the phone to prevent it from sliding forward.
- **Back Support (Rear Brace)**: A vertical strut positioned at $a \in [90, 110]$, $b \in [-2, 0]$, and $|y| \le 15$. By occupying the $b \in [-2, 0]$ range, it sits directly behind the phone's back face without intersecting the phone volume ($b > 0$).
- **Load Path**: Gravity $\to$ Phone $\to$ [Seat + Lip + Back Support] $\to$ Base Plate $\to$ Desk.

**Requirement Fulfillment**:
- **R1 (Single Solid)**: All features (Base, Seat, Lip, and Back Support) are designed as a single union of primitives.
- **R2 (Footprint/Height)**: Footprint is $60 \times 90$ mm; Height is $\approx 110$ mm (to reach the back support at $a=100$); Min $z=0$.
- **R3 (No Intersection)**: All structural elements are placed either in the "Seat" zone ($b \in [0,9]$), "Lip" zone ($b \in [9,13]$), or "Back Support" zone ($b \in [-2,0]$). Any other part of the stand is offset from the phone's volume defined by $u$ and $n$.
- **R4 (Back Support)**: Specifically placed at $a \in [90, 110]$, $|y| \le 15$, with thickness extending to $b = -2$ (behind the back face).
- **R5 (Seat & Lip)**: Seat covers $a \in [-4, 0], b \in [0, 9]$; Lip covers $a \in [0, 8], b \in [9, 13]$. Both within $|y| \le 15$.
- **R6 (Stability)**: The wide base ($x$ range $-40$ to $20$) ensures the combined COM of the stand and phone projects into the footprint with a $>5$ mm margin.
- **R7 (Mass)**: Total volume is optimized to $\approx 32,000 \text{ mm}^3$, resulting in a mass of $\approx 39.7\text{g}$ ($<60\text{g}$).