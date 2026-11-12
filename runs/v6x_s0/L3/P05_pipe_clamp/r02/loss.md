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