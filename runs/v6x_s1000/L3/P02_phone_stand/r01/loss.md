## Verdicts
R1: PASS - 1 solid found in STEP file.
R2: FAIL - x-extent 126.4mm > 100mm, height 311.9mm > 120mm, min z -11.9mm < 0.
R3: FAIL - 2868 intersection points detected.
R4: UNSURE - Simulation check is unfaithful to specification.
R5: UNSURE - Simulation check is unfaithful to specification.
R6: FAIL - Combined COM x (-2.23) does not project into contact area x [0, 0].
R7: FAIL - Mass 4005.15g > 60g.

## Problems
- Mass: 4005.15 g (should be <= 60 g).
- Height: 311.9 mm (should be <= 120 mm).
- Footprint Width: 126.4 mm (should be <= 100 mm).
- Minimum Z: -11.9 mm (should be >= 0).
- Phone Intersection: 2868 points (should be 0).
- Stability: COM projection outside contact area (should be inside with 5mm margin).

SIM_CODE_ISSUE: yes