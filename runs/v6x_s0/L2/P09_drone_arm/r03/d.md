**Concept**: A tapered I-beam drone arm constructed via a series of extruded segments (or a swept profile) along the X-axis to ensure geometric stability and avoid lofting errors. The cross-section is designed with thin webs and flanges to minimize mass while maintaining high stiffness.

**Main Features**:
- **Profile Construction**: A tapered I-beam shape created by extruding/sweeping a profile from $x=0$ to $x=130$. To ensure R1, the geometry is generated as a single solid, and all holes are integrated using `cut` operations.
- **Wall Thicknesses**: Web thickness = $1.5\text{ mm}$, Flange thicknesses (top and bottom) = $2.0\text{ mm}$.
- **Frame Attachment**: Two $\varnothing 3.2\text{ mm}$ vertical holes created via `cut` at $(6, \pm 6)$.
- **Motor Mount**: Four $\varnothing 3.2\text{ mm}$ vertical holes created via `cut` at $(112, \pm 9.5)$, $(128, \pm 9.5)$, and one central $\varnothing 6\text{ mm}$ vertical shaft hole at $(120, 0)$.
- **Dimensions**: Length $130\text{ mm}$, height $14\text{ mm}$, width tapers from $30\text{ mm}$ (at frame) to $20\text{ mm}$ (at motor).

**Load Path**: The motor thrust at $x=120$ creates a bending moment. The load travels through the vertical webs of the I-beam towards the frame attachment points at $x=6$.

**Requirement Fulfillment**:
- R1: Created as a single continuous solid using extrusion/sweep logic, with holes subtracted via boolean `cut`.
- R2: Envelope is approximately $130 \times 30 \times 14\text{ mm}$, within limits.
- R3: Holes placed at $(6, \pm 6)$ with diameter $3.2\text{ mm}$.
- R4: Motor holes at $(112, \pm 9.5)$, $(128, \pm 9.5)$, and shaft hole at $(120, 0)$ are all vertical clearance holes.
- R5: At $x=20$, with height $H=14\text{ mm}$, width $W \approx 28\text{ mm}$, flange thickness $t_f=2\text{ mm}$, and web thickness $t_w=1.5\text{ mm}$:
  $I \approx \frac{W H^3}{12} - \frac{(W-t_w)(H-2t_f)^3}{12} \approx 460\text{ mm}^4$.
  $Z = I / (H/2) \approx 65.7\text{ mm}^3$.
  $\sigma = M/Z = 1200 / 65.7 \approx 18.3\text{ MPa} < 30\text{ MPa}$.
- R6: At $x=20$, $I \approx 460\text{ mm}^4$, which is $\gg 1.0\text{ mm}^4$.
- R7: Estimated volume $\approx 15\text{ cm}^3$. Mass $\approx 15 \times 1.24 = 18.6\text{ g} < 20\text{ g}$.