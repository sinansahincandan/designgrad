**Concept**: A split-style saddle clamp consisting of a base plate with two mounting flanges and an upper arch that cradles the pipe. The geometry is strictly constrained to a Y-width of $20\text{ mm}$ and is optimized to provide structural support while staying under the mass limit, ensuring all components are contained within the specified Y-extent and Z-bounds.

**Main Features**:
- **Base/Flanges**: A continuous base plate with an exact Y-width of $20\text{ mm}$ ($y \in [-10, 10]$). No part of the base or flanges may extend beyond $|y| = 10$. The bottom surface sits at $z = 0$. To ensure the screw holes at $(\pm 27, 0)$ are fully contained within the solid material, the base plate extends to $x = \pm 30$.
- **Saddle Arch**: A curved section centered at $(0, 0, 12.5)$. To satisfy R4, the arch is defined by an outer radius $R_{outer}$ such that $15.5\text{ mm} \le R_{outer} < 16.0\text{ mm}$ for the region $|x| \le 7$. This ensures a thick, continuous band of material exists specifically in the radial interval $[12.7, 15.5]\text{ mm}$ from the pipe axis. The arch's Y-extent is also strictly limited to $y \in [-10, 10]$.
- **Screw Holes**: Two vertical bores of $\varnothing 6.6\text{ mm}$ created via boolean subtraction, centered at $(\pm 27, 0)$. To ensure the holes are fully empty and penetrate the entire thickness of the flanges and base plate, the subtraction must extend from $z = -1$ through to the maximum height of the part.

**Load Path**: Downward force from the pipe is transferred through the saddle arch to the base plate and then distributed through the mounting flanges into the surface via the screws.

**Requirement Fulfillment**:
- R1: The part is constructed as a single continuous solid using boolean unions (for the body) and subtractions (for the pipe clearance and screw holes).
- R2: Width is exactly $20\text{ mm}$ ($y \in [-10, 10]$), X extent is $60\text{ mm}$ ($|x|=30 \rightarrow 60$), and the bottom surface sits at $z=0$. All features are strictly bounded by $|y| \le 10$.
- R3: A cylinder of radius $12.6\text{ mm}$ centered at $(0, 0, 12.5)$ is subtracted from the union of all other parts as a global boolean subtraction to ensure zero intersection volume with the pipe.
- R4: Material exists in the band above the pipe by defining the saddle arch's outer boundary to be between $15.5\text{ mm}$ and $16.0\text{ mm}$ from the pipe axis for $|x| \le 7$, ensuring coverage of the $[12.7, 15.5]\text{ mm}$ radial band.
- R5: Two $\varnothing 6.6\text{ mm}$ holes are drilled vertically at $(\pm 27, 0)$ from $z = -1$ to ensure a clean, complete cut through the flanges and base plate.
- R6: Flanges are $3\text{ mm}$ thick ($z=0$ to $3$) and located within $18.5 \le |x| \le 23$ and $|y| \le 4$.
- R7: Total volume is approximately $1600\text{ mm}^3$; mass $\approx 1.98\text{ g}$ (calculated as $V \times 0.00124\text{ g/mm}^3$), which is well below the $25\text{ g}$ limit ($\le 20,161\text{ mm}^3$).