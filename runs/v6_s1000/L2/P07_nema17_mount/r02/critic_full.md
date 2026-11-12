## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The face plate thickness is correct ($y=0$ to $4$), but the "solid material all around the central bore" requirement is failed. Evidence shows a filled fraction of only 0.36 for the ring surrounding the bore, meaning the bore has consumed most or all of the material in that region.
- R3: FAIL. The central bore diameter should be 22.5 mm (radius 11.25). Evidence shows an empty volume fraction of 0.0 and wall presence of 0.36 for a cylinder with radius 11.25, implying the hole is not actually present or the material around it is missing.
- R4: FAIL. The holes are at $(x, z) = (\pm 15.5, 30 \pm 15.5)$. Evidence shows the simulation checked coordinates $(\pm 15.5, 45.5)$ and $(\pm 15.5, 14.5)$, which matches $30+15.5$ and $30-15.5$. However, the wall presence is only 0.4, indicating the holes are not properly formed or the face plate material is insufficient.
- R5: PASS. Intersection volume with clearance box is 0.0.
- R6: FAIL. The base must be on the table ($z \ge 0$). Evidence shows $z_{min}$ check failed (value 0.0, but note implies a failure in hole/wall fraction). More importantly, the holes at $(\pm 25, 25)$ have a wall presence of only 0.133, meaning they are not properly integrated or the base is too thin/missing material.
- R7: PASS. Envelope $x \in [-35, 35]$, $z_{max} = 55$ and mass $\approx 48.5$ g (under 60g) are met.

## Verdicts
R1: PASS - Counted 1 solid.
R2: FAIL - Material fraction around central bore is only 0.36, failing the "solid material all around" requirement.
R3: FAIL - Bore diameter/presence check failed (wall presence 0.36).
R4: FAIL - Motor hole wall presence is only 0.4.
R5: PASS - No intersection with clearance volume.
R6: FAIL - Base screw holes have insufficient wall presence (0.133).
R7: PASS - Envelope and mass are within limits.

## Problems
- Face Plate Integrity: The material surrounding the central bore and motor screw holes is insufficient (wall fractions 0.36 and 0.4 respectively); the face plate must be solid around these features.
- Base Screw Holes: The vertical holes at $(\pm 25, 25)$ have insufficient wall presence (0.133).

SIM_CODE_ISSUE: no