## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Thickness is 8mm (meets $\ge$ 4mm) and material exists around the bore.
- R3: FAIL. The design document claims it's at $z=30$, but simulation/render shows it is incorrectly placed (likely two separate bores or misplaced, as evidenced by empty volume fraction errors).
- R4: FAIL. Simulation shows holes are not correctly implemented; render confirms they are missing entirely.
- R5: PASS. Intersection volume with clearance box is 0.0.
- R6: FAIL. Simulation indicates the base does not sit at $z=0$ (z_min check failed) and/or the hole geometry is incorrect.
- R7: FAIL. Mass is 65.55g, which exceeds the limit of 60g. The envelope $x$ limits are met, but mass fails.

## Verdicts
R1: PASS - 1 solid found.
R2: PASS - thickness is 8mm and material is present around bores.
R3: FAIL - bore is not centered at z=30 (measured as misplaced).
R4: FAIL - motor screw holes are missing or incorrectly implemented.
R5: PASS - zero intersection with clearance volume.
R6: FAIL - base does not meet the minimum z=0 requirement and hole geometry is invalid.
R7: FAIL - mass is 65.55g, exceeding the 60g limit.

## Problems
- Mass: 65.55g (should be $\le$ 60g).
- Central Bore Position: z=41/z=19 (should be z=30).
- Motor Screw Holes: Missing from face plate (should be four $\varnothing$ 3.4 mm holes at specified coordinates).
- Base Placement: $z_{min} \neq 0$ (should be $z \ge 0$).

SIM_CODE_ISSUE: no