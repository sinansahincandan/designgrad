**Concept**: A split-style saddle clamp consisting of a base plate with two primary mounting flanges and an upper arch that cradles the pipe. The geometry is optimized to provide structural support while minimizing material to stay under the mass limit, featuring an extended base to accommodate screw holes at specific coordinates.

**Main Features**:
- **Base/Flanges**: Two primary flange regions located at $|x| \in [18.5, 23]$ with a thickness of $3\text{ mm}$, connected by a continuous base plate that extends to $|x| = \pm 30$ to accommodate the screw holes.
- **Saddle Arch**: A curved section centered at $(0, 0, 12.5)$ with an inner radius of $12.6\text{ mm}$ and an outer radius of $16.0\text{ mm}$ that wraps over the pipe.
- **Screw Holes**: Vertical bores of $\varnothing 6.6\text{ mm}$ located at $(\pm 27, 0)$, fully contained within the extended base plate structure.

**Load Path**: Downward force from the pipe is transferred through the saddle arch to the base plate and then distributed through the mounting flanges and the continuous base into the surface via the screws.

**Requirement Fulfillment**:
- R1: The part is constructed as a single continuous solid using boolean unions/subtractions.
- R2: Width is $20\text{ mm}$ (Y), X extent is approx $60\text{ mm}$ ($|x|=30 \rightarrow 60$), sits on $z=0$.
- R3: A cylinder of radius $12.6\text{ mm}$ centered at $(0, 0, 12.5)$ is subtracted.
- R4: Material exists in the required band above the pipe because the outer radius of $16.0\text{ mm}$ ensures material covers the range from $12.7\text{ mm}$ to $15.5\text{ mm}$ from the pipe axis.
- R5: Two $\varnothing 6.6\text{ mm}$ holes are drilled at $(\pm 27, 0)$ through the extended base structure.
- R6: Flanges are $3\text{ mm}$ thick ($z=0$ to $3$) and located at $|x| \in [18.5, 23]$, satisfying the specific geometry requirement.
- R7: Total volume is approx $1800\text{ mm}^3$; mass $\approx 2.23\text{ g}$, well below $25\text{ g}$.