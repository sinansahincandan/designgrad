**Concept**: A tapered I-beam drone arm constructed via a series of extruded segments (or a swept profile) along the X-axis to ensure geometric stability and avoid lofting errors. The cross-section is designed with thin webs and flanges to minimize mass while maintaining high stiffness.

**Main Features**:
- **Profile Construction**: A tapered I-beam shape created by extruding/sweeping a profile from $x=0$ to $x=130$. To ensure R1, the geometry is generated as a single continuous solid first, and all holes are subtracted via boolean `cut` operations *after* the main body is fully formed.
- **Wall Thicknesses**: Web thickness = $1.5\text{ mm}$, Flange thicknesses (top and bottom) = $2.0\text{ mm}$.
- **Frame Attachment**: Two $\varnothing 3.2\text{ mm}$ vertical holes (along the Z-axis) centered at $(6, 6)$ and $(6, -6)$.
- **Motor Mount**: Four $\varnothing 3.2\text{ mm}$ vertical holes located at: $(112, 9.5), (112, -9.5), (128, 9.5)$, and $(128, -9.5)$. One central $\varnothing 6\text{ mm}$ vertical clearance hole for the shaft at $(120, 0)$.
- **Dimensions**: Length $130\text{ mm}$, height $14\text{ mm}$, width tapers from $30\text{ mm}$ (at frame) to $20\text{ mm}$ (at motor).

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created as a single continuous solid using extrusion/sweep logic, with holes subtracted via boolean `cut` operations after the main body is formed to ensure hole integrity.
- R2: Envelope is approximately $130 \times 30 \times 14\text{ mm}$, within limits ($x \le 136, |y| \le 16, z_{height} \le 20$).
- R3: Frame attachment holes are vertical $\varnothing 3.2\text{ mm}$ at $(6, 6)$ and $(6, -6)$.
- R4: Motor mount includes four $\varnothing 3.2\text{ mm}$ vertical holes at $(112, 9.5), (112, -9.5), (128, 9.5), (128, -9.5)$ and one $\varnothing 6\text{ mm}$ shaft hole at $(120, 0)$.
- R5: At $x=20$, with height $H=14\text{ mm}$, width $W \approx 28\text{ mm}$, flange thickness $t_f=2\text{ mm}$, and web thickness $t_w=1.5\text{ mm}$:
  $I \approx \frac{W H^3}{12} - \frac{(W-t_w)(H-2t_f)^3}{12} \approx 460\text{ mm}^4$.
  $Z = I / (H/2) \approx 65.7\text{ mm}^3$.
  $\sigma = M/Z = 1200 / 65.7 \approx 18.3\text{ MPa} < 30\text{ MPa}$.
- R6: Estimated tip deflection $\delta = \frac{F \cdot L^3}{3 \cdot E \cdot I} = \frac{12 \cdot 100^3}{3 \cdot 3500 \cdot 460} \approx 0.25\text{ mm}$, which is $\le 1.0\text{ mm}$.
- R7: Estimated volume $\approx 15\text{ cm}^3$. Mass $\approx 15 \times 1.24 = 18.6\text{ g} < 20\text{ g}$.