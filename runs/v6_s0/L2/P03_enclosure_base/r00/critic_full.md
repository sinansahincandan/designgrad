## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Simulation confirms floor exists from z=0 to z=2 under the board area.
- R3: UNSURE. The simulation check for R3 was flagged as non-faithful (it only checked if volume is zero, not if the region is actually empty of material). I cannot verify this via the provided evidence.
- R4: PASS. Bounding box measurements [85, 55, 31] match requirements.
- R5: FAIL. Simulation probe shows both OD and pilot hole requirements failed for all four bosses. The design document claims OD 6mm and 2.2mm holes, but the measured evidence contradicts this.
- R6: FAIL. Simulation reports `opening_intersected: 0.0`. This means the cutout did not actually penetrate/intersect the wall material, despite the design doc claiming it exists.
- R7: PASS. Measured mass is 65.47g, which is $\le$ 70g.

## Verdicts
R1: PASS - Evidence confirms 1 solid.
R2: PASS - Evidence confirms floor thickness and coverage.
R3: UNSURE - Simulation check was non-faithful; cannot verify if region is empty.
R4: PASS - Measured dimensions [85, 55, 31] meet spec.
R5: FAIL - Measured probe shows OD and pilot hole requirements are not met.
R6: FAIL - Measured opening intersection is 0.0, meaning no cutout exists in the wall.
R7: PASS - Measured mass 65.47g $\le$ 70g.

## Problems
- USB-C Cutout (R6): The cutout does not intersect/penetrate the wall; it must create an opening through the $-X$ face.
- Screw Bosses (R5): Outer diameter and pilot hole dimensions do not meet specification (OD $\ge$ 6mm, hole $\ge$ 2.2mm dia and $\ge$ 4mm deep).

SIM_CODE_ISSUE: no