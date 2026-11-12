## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured X extent is ~100 mm (limit $\le$ 80) and Y extent is ~31 mm (limit 18-22). Zmin is -3, meaning it does not sit on $z=0$.
- R3: FAIL. Intersection volume with the pipe cylinder is non-zero ($0.10\text{ mm}^3$), meaning material exists where it should be free.
- R4: FAIL. The intersection volume of the required band and $|x| \le 7$ is $0.399$, which is not the full shell volume, implying the material is missing in that region.
- R5: FAIL. Simulation shows holes are not empty or lack surrounding material at $(\pm 27, 0)$.
- R6: FAIL. The intersection with the flange probe box is false (zero), meaning the flanges do not exist where required.
- R7: FAIL. Mass is $31.54\text{ g}$ (limit $\le 25\text{ g}$). Note: The design document claims a volume of $1600\text{ mm}^3$, but simulation shows $25432\text{ mm}^3$. This is a massive discrepancy.

## Verdicts
R1: PASS - 1 solid found.
R2: FAIL - X extent is 100 mm (limit $\le$ 80), Y extent is 31 mm (limit 18-22), and Zmin is -3 (must be 0).
R3: FAIL - Non-zero intersection volume with pipe cylinder.
R4: FAIL - Material missing in the required band for $|x| \le 7$.
R5: FAIL - Screw holes at $(\pm 27, 0)$ are invalid.
R6: FAIL - Flanges do not exist in the specified region.
R7: FAIL - Mass is 31.54 g (limit $\le$ 25 g).

## Problems
- Mass/Volume: Measured mass is 31.54 g; should be $\le$ 25 g.
- Dimensions: X extent is 100 mm; should be $\le$ 80 mm. Y extent is 31 mm; should be 18-22 mm.
- Z-Position: Zmin is -3; must sit on $z=0$.
- Pipe Clearance: Material exists in the pipe volume (R3).
- Saddle Band: Material missing in the band $12.7$ to $15.5\text{ mm}$ for $|x| \le 7$.
- Flanges: No material found in specified flange regions ($18.5 \le |x| \le 23, |y| \le 4, z \in [0,3]$).
- Screw Holes: Holes at $(\pm 27, 0)$ are not correctly formed.

SIM_CODE_ISSUE: yes