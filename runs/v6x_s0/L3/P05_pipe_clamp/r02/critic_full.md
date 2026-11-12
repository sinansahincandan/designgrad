## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. Measured Y extent is 31 mm, exceeding the limit of 22 mm. Also, Zmin is -7.5 mm; the requirement states it must sit on z=0 (implying Zmin >= 0). The X extent (54 mm) is fine.
- R3: FAIL. Measured intersection volume with the pipe cylinder is non-zero (0.106), meaning material exists where the pipe should be.
- R4: FAIL. Measured intersection volume with the required band is non-zero (0.186), meaning the required material is missing from that band.
- R5: FAIL. Simulation shows holes are not empty/correctly formed at (+-27, 0). The design claims they are vertical bores through flanges, but evidence contradicts this.
- R6: PASS. Measured intersection with probe boxes confirms flange thickness and location requirements are met.
- R7: PASS. Mass is ~14.45 g, which is <= 25 g.

## Verdicts
R1: PASS - Counted 1 solid in STEP file.
R2: FAIL - Y extent is 31 mm (limit 22 mm) and Zmin is -7.5 mm (must be 0).
R3: FAIL - Non-zero intersection volume detected within the pipe radius.
R4: FAIL - Material missing from the specified band (intersection volume < 1).
R5: FAIL - Holes at (+-27, 0) are not correctly formed/empty as required.
R6: PASS - Flange geometry meets thickness and location requirements.
R7: PASS - Mass is 14.45 g (limit 25 g).

## Problems
- Mounting Surface: Zmin is -7.5 mm; should be 0 mm.
- Clamp Width: Y extent is 31 mm; should be between 18 and 22 mm.
- Pipe Cavity: Material exists in the pipe volume (R=12.6); should be free of material.
- Saddle Band: Material is missing from the band 12.7 to 15.5 mm from axis; should be solid.
- Screw Holes: Holes at (+-27, 0) are not correctly formed vertical bores.

SIM_CODE_ISSUE: no