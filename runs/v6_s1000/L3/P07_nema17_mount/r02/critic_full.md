## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The face plate thickness is correct ($y=0$ to $4$), but the simulation shows a material fraction of only 0.371 around the central bore, indicating the bore/holes have compromised the "solid material all around" requirement or the geometry is insufficient.
- R3: FAIL. Simulation reports an empty volume fraction for the central bore, implying it is not correctly implemented as a through-hole or is misaligned.
- R4: FAIL. Simulation shows 0.4 volume fraction for all four holes; combined with the visual reviewer report of only two visible holes, this indicates the holes are either incorrectly placed, incomplete, or improperly subtracted.
- R5: PASS. Intersection volume with clearance box is 0.0.
- R6: FAIL. Simulation shows $z_{min}$ issues and incorrect hole properties/presence for the specified coordinates $(\pm 25, 25)$. Visual evidence also suggests holes are missing or incorrect diameter.
- R7: PASS. BBox and mass ($43.51\text{g} \le 60\text{g}$) are within limits.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Material fraction around central bore is only 0.371, failing the "solid material all around" requirement.
R3: FAIL - Simulation shows empty volume fraction for the central bore at (0,0,30).
R4: FAIL - Simulation and visual inspection show incorrect implementation/presence of the four motor holes.
R5: PASS - No intersection with clearance zone.
R6: FAIL - Simulation shows $z_{min}$ issues and incorrect hole geometry at $(\pm 25, 25)$.
R7: PASS - Envelope and mass are within specification limits.

## Problems
- R3/R4 (Motor Holes): Central bore and motor screw holes are not correctly implemented as through-holes in the face plate.
- R6 (Base Holes): Vertical screw holes at $(\pm 25, 25)$ are missing or have incorrect diameter/placement.
- R2 (Face Plate Integrity): Insufficient material remains around the central bore.

SIM_CODE_ISSUE: no