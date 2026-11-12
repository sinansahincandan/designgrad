## Working
- **R1**: The design specifies a union of two blocks (Face Plate and Base Plate). This satisfies the requirement for one single solid.
- **R2**: Face plate is defined as $y \in [0, 4]$. Thickness = 4 mm. Material around central bore depends on whether the bore/motor holes intersect the edges. Bore center $(0,30)$, radius 11.25. Plate width $x \in [-35, 35]$ (70mm). Distance from center to edge is 35mm. $35 - 11.25 = 23.75$ mm of material remains. PASS.
- **R3**: Central bore diameter $\varnothing 22.5$ mm at $(0, 30)$ is stated. PASS.
- **R4**: Four holes $\varnothing 3.4$ mm at $(\pm 15.5, 30 \pm 15.5)$. Coordinates match specification exactly. PASS.
- **R5**: Clearance volume $x \in [-21.5, 21.5], y \in [-48, 0], z \in [8.5, 51.5]$ is subtracted. This ensures nothing exists in that space. PASS.
- **R6**: Two vertical holes $\varnothing 5.5$ mm at $(\pm 25, 25)$. Base plate $y \in [4, 50]$. Hole center $y=25$ is within the base plate range. $x=\pm 25$ is within $x \in [-35, 35]$. PASS.
- **R7 (Envelope)**: $x \in [-35, 35]$ (Width 70). $z_{max} = 55$. Matches specification.
- **R7 (Mass)**: 
    - Face Plate Volume: $70 \times 4 \times 55 = 15,400 \text{ mm}^3$.
    - Base Plate Volume: $70 \times 46 \times 4 = 12,880 \text{ mm}^3$.
    - Total raw volume $\approx 28,280 \text{ mm}^3$.
    - Subtracting holes and clearance (approximate):
        - Central bore: $\pi \cdot 11.25^2 \cdot 4 \approx 1,590 \text{ mm}^3$.
        - Motor holes: $4 \cdot \pi \cdot 1.7^2 \cdot 4 \approx 145 \text{ mm}^3$.
        - Table holes: $2 \cdot \pi \cdot 2.75^2 \cdot 46 \approx 2,180 \text{ mm}^3$.
        - Clearance volume (partially in face plate): The clearance is $y < 0$, but the face plate starts at $y=0$. However, R5 specifies a volume for *nothing* to exist. If the design subtracts this from the solid, it only affects material where $y \ge 0$. Since the face plate is $y \in [0,4]$, and the clearance is $y \in [-48, 0]$, there is no overlap between the clearance volume and the bracket material.
    - Estimated Volume $\approx 28,280 - 1,590 - 145 - 2,180 = 24,365 \text{ mm}^3$.
    - Mass $= 24,365 \text{ mm}^3 \times (1.24 \text{ g} / 1000 \text{ mm}^3) = 30.21 \text{ g}$.
    - The design claims to use "pocketing" to ensure mass $< 60\text{g}$, but even without pocketing, the mass is $\approx 30\text{g}$. PASS.

## Verdicts
R1: PASS - Union of two blocks used.
R2: PASS - Thickness is 4 mm ($y=0$ to $4$).
R3: PASS - Diameter 22.5 mm at $(0, 30)$.
R4: PASS - Four $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$.
R5: PASS - Clearance volume subtracted.
R6: PASS - Two $\varnothing 5.5$ mm holes at $(\pm 25, 25)$.
R7: PASS - Envelope $x \in [-35, 35], z_{max}=55$; Mass $\approx 30\text{g} < 60\text{g}$.

## Problems
None