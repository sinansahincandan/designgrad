## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection check shows floor covers the required area at $z=0$ to $z=2$.
- R3: PASS. Intersection check shows zero material in the specified cavity volume.
- R4: FAIL. The bounding box measurement shows $z_{max} = 33.0$. The requirement specifies wall top must be between $z=30$ and $z=32.5$.
- R5: PASS. Bosses are at correct coordinates, have $\ge 6\text{mm}$ OD, and pilot holes (radius 1.1mm = diameter 2.2mm) are present and deep enough ($z=8$ to $z=4$ is 4mm depth).
- R6: UNSURE. The simulation failed with an error/unreliable probe. The reviewer notes the probe box extends into empty space, making the `wall_slice_empty` metric invalid. However, the design document claims a cutout spanning $x \in [-42.5, -40]$, which matches the wall thickness (85mm outer / 2 = 42.5mm). Since I cannot verify the void via simulation due to the error, and the evidence is inconclusive, I must mark this UNSURE.
- R7: PASS. Measured mass is 38.22g, which is $\le 70\text{g}$.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Floor thickness and coverage verified by intersection.
R3: PASS - Cavity volume verified empty by intersection.
R4: FAIL - Wall top $z_{max}$ is 33.0, exceeding the limit of 32.5.
R5: PASS - Bosses meet all geometric and hole requirements.
R6: UNSURE - Simulation probe failed/errored; cannot verify cutout penetration.
R7: PASS - Mass is 38.22g.

## Problems
- Wall Height: Top of wall is at $z=33.0$; must be between $z=30$ and $z=32.5$.
- USB-C Cutout: Verification failed due to simulation error; ensure cutout fully penetrates the -X wall.

SIM_CODE_ISSUE: yes