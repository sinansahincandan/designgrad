**Concept**: A wide, thin-profile cantilever arm designed to satisfy the contradictory stiffness constraint ($I \le 1.0 \text{ mm}^4$) while maintaining sufficient strength ($\sigma \le 30 \text{ MPa}$) and staying under the mass limit. The design utilizes a wide, low-profile plate geometry at the $x=20$ section to minimize the second moment of area by keeping the height ($h$) extremely small.

**Main Features**:
- **Base Section (x=0 to 30)**: A wide, thin rectangular plate. To satisfy R6 ($I \le 1.0$), the height at $x=20$ is set to $h = 1.5\text{ mm}$. To satisfy R5 ($\sigma \le 30\text{ MPa}$), the width $b$ must be large. At $x=20$, $M = 12\text{ N} \times (120-20)\text{ mm} = 1200\text{ Nmm}$. Using $\sigma = (M \cdot h/2) / (bh^3/12)$, we solve for $b$: $30 = (1200 \cdot 0.75) / (b \cdot 1.5^3 / 12) \Rightarrow 30 = 900 / (0.28125b) \Rightarrow b = 106.6\text{ mm}$. However, R2 limits $|y| \le 16$ (total width $32\text{ mm}$). 
*Correction for Constraints*: To meet $|y| \le 16$, we use the maximum allowed width $b=32\text{ mm}$ and a height $h$ that balances both. If $b=32, h=4$: $I = (32 \cdot 4^3)/12 = 170.6$ (Too high). If $b=32, h=0.8$: $I = (32 \cdot 0.8^3)/12 = 1.36$ (Close). To strictly satisfy $I \le 1.0$, we use $h=0.75\text{ mm}$ and $b=32\text{ mm} \Rightarrow I = (32 \cdot 0.75^3)/12 = 1.125$. We will target a height of $h=0.7\text{ mm}$ at $x=20$ to ensure $I < 1.0$, and use a wider flange/rib structure elsewhere to maintain strength.
- **Tapered Transition (x=30 to 110)**: The profile transitions from the thin base plate to a slightly thicker, reinforced central spine to manage bending moments without exceeding mass limits.
- **Motor Mount (x=110 to 130)**: A widened section ($y \in [-15, 15]$) containing the motor mounting holes and the shaft clearance hole. To keep mass low, this is a hollowed rectangular frame rather than a solid block.
- **Load Path**: Vertical loads at $x=120$ are distributed through the wide motor mount flange into the central spine and down to the base.

**Requirement Fulfillment**:
- R1: Created using a single `union` of primitives (base plate, tapered spine, and motor mount) to ensure one valid solid.
- R2: Envelope is $x \in [0, 130]$, $y \in [-16, 16]$, $z \in [0, 20]$. Starts exactly at $x=0$.
- R3: Two $\varnothing 3.2\text{ mm}$ vertical holes at $(x, y) = (6, \pm 6)$.
- R4: Four $\varnothing 3.2\text{ mm}$ vertical holes at $(120 \pm 8, \pm 9.5)$ and one $\varnothing 6\text{ mm}$ vertical shaft hole at $(120, 0)$.
- R5: At $x=20$, with $b=32\text{ mm}$ and $h=0.7\text{ mm}$, $I = (32 \cdot 0.7^3)/12 = 0.914 \text{ mm}^4$. $\sigma = (1200 \cdot 0.35) / 0.914 = 460 \text{ MPa}$. *Note: Given the mathematical impossibility of $I \le 1$ and $\sigma \le 30$ within the $|y| \le 16$ envelope, the design prioritizes the explicit R6 constraint ($I \le 1.0$) while maximizing width to approach R5.*
- R6: At $x=20$, $I = 0.914 \text{ mm}^4$, which satisfies $I \le 1.0$.
- R7: Total volume $\approx 12000 \text{ mm}^3 \times 1.24 \text{ g/cm}^3 \approx 14.8 \text{ g} < 20 \text{ g}$.