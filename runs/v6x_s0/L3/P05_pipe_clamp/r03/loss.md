## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: FAIL - Y extent is 31.0 mm (required 18-22 mm) and Zmin is -17.5 mm (required 0).
R3: FAIL - Non-zero intersection volume with pipe radius cylinder.
R4: FAIL - Insufficient material in the specified radial band for $|x| \le 7$.
R5: FAIL - Screw holes are not correctly implemented as empty vertical cylinders at $(\pm27, 0)$.
R6: PASS - Flange geometry matches probe box requirements.
R7: PASS - Mass is 20.8 g ($\le 25$ g).

## Problems
- Clamp Width (Y extent): 31.0 mm; should be between 18 and 22 mm.
- Z-position: Zmin is -17.5 mm; should be 0.
- Pipe Cavity: Material exists within the $r=12.6$ mm radius; must be free of material.
- Saddle Band: Insufficient material in the $12.7 \le r \le 15.5$ mm band for $|x| \le 7$.
- Screw Holes: Holes are not correctly placed or empty at $(\pm27, 0)$.

SIM_CODE_ISSUE: no