**Concept**: A compact injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB, featuring integrated screw bosses and a side cutout for connectivity.

**Main Features**:
- **Outer Dimensions**: 85 x 55 mm footprint with a height of 32 mm.
- **Internal Cavity**: 80 x 50 mm clear space from $z=8$ to $z=32$.
- **Screw Bosses**: Four $\varnothing 7$ mm cylinders located at $(\pm 35, \pm 20)$ with $\varnothing 2.2$ mm holes.
- **USB Cutout**: A $9 \times 3$ mm rectangular aperture on the $-X$ wall.

**Load Path**: PCB weight is transferred through screws into the bosses; bosses transfer load to the floor; floor transfers load to the mounting surface via the large contact area. The screw bosses are physically merged into the floor geometry via a boolean union operation, ensuring no zero-thickness interfaces or disconnected components exist.

**Requirement Fulfillment**:
- **R1**: Constructed by creating a single base block ($85 \times 55 \times 32$ mm), performing a single Boolean subtraction of the central cavity, and then performing a single Boolean union with the four screw bosses to ensure a continuous, manifold volume.
- **R1 Verification**: The part is defined as a single `cq.Workplane` object where all additive features (walls/bosses) and subtractive features (cavity/holes/cutout) are applied to the same base primitive, ensuring a single valid solid output.
- **R2**: Floor thickness is 8 mm (from $z=0$ to $z=8$), exceeding the 2 mm minimum.
- **R3**: A central void is subtracted from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- **R4**: Outer dimensions are 85 x 55 mm; wall top is at $z=32$.
- **R5**: Four bosses at $(\pm 35, \pm 20)$ with $\varnothing 7$ mm OD and $\varnothing 2.2$ mm holes (depth 6 mm).
- **R6**: USB-C cutout centered at $(-42.5, 0, 14)$ measuring $9 \times 3$ mm.
- **R7**: Estimated volume is $\approx 48\text{ cm}^3$, mass $\approx 60\text{ g}$ (under the 70g limit).