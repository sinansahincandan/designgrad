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