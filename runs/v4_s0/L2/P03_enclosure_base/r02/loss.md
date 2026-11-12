R1: PASS - 1 solid found.
R2: PASS - Intersection volume of floor region is 8000.0 mm3.
R3: PASS - Intersection volume of board cavity is 0.0 mm3.
R4: PASS - Bounding box [85.0, 55.0, 31.0] meets specs.
R5: FAIL - Verified bosses show 0 valid bosses; the pilot hole depth/location logic failed to produce required geometry.
R6: FAIL - Intersection volume with cutout probe is 27.0 mm3 (should be 0.0 mm3 for a void).
R7: PASS - Mass is 65.5g, which is <= 70g.

Most important problems to fix:
- USB-C Cutout: The cutout is not actually open; the probe found 27.0 mm3 of material in the cutout region.
- Screw Bosses: No valid bosses were detected by the verification method (value=0).

SIM_CODE_ISSUE: no