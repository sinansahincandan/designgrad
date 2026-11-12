## Working
- R1: The simulation confirms 1 solid. PASS.
- R2: Measured x-extent is 126.4 mm (> 100 mm), z-height is 311.9 mm (> 120 mm), and min z is -11.9 mm (< 0). FAIL.
- R3: Simulation found 2868 intersection points within the phone volume. FAIL.
- R4: The simulation check was deemed unfaithful/unreliable by the reviewer. UNSURE.
- R5: The simulation check was deemed unfaithful/unreliable by the reviewer. UNSURE.
- R6: Combined COM x is -2.23 mm. Contact area x-range is [0.0, 0.0]. The projection falls outside the contact area. FAIL.
- R7: Measured mass is 4005.15 g (Volume 3,229,959.55 mm³ * 0.00124). This is far above the 60 g limit. FAIL.

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