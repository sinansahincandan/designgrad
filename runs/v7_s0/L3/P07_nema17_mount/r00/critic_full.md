## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The render shows the face plate thickness extends from $y=0$ to $y=50$, whereas the spec requires $y=0$ to $4$. Even if the simulation probe failed due to a bad check, the visual evidence of orientation is definitive.
- R3: PASS. Simulation confirms central bore exists and is empty (through-hole).
- R4: FAIL. The render shows large circular recesses/cutouts instead of 3.4 mm holes at the specified coordinates. Simulation also failed to find these holes.
- R5: PASS. Simulation confirms zero intersection with the motor clearance volume.
- R6: FAIL. The simulation measures $z_{min} = -27.5$, which violates "minimum $z=0$". The render confirms the base is below the table ($z < 0$). Additionally, the hole existence check failed.
- R7: PASS. Simulation confirms envelope and mass are within limits (though the orientation is wrong, the dimensions/mass values provided by simulation are used).

## Verdicts
R1: PASS - Evidence from simulation.
R2: FAIL - Render shows face plate thickness extends to $y=50$ instead of $y=4$.
R3: PASS - Evidence from simulation.
R4: FAIL - Render shows large recesses instead of 3.4 mm holes; simulation failed to find them.
R5: PASS - Evidence from simulation.
R6: FAIL - Simulation and render show base at $z = -27.5$ instead of $z \ge 0$.
R7: PASS - Evidence from simulation.

## Problems
- Orientation/Placement: Base is at $z = -27.5$, should be $z \ge 0$.
- Face Plate Thickness: Extends to $y=50$, should be $y=4$.
- Motor Screw Holes: Large circular recesses instead of $\varnothing 3.4$ mm holes at $(\pm 15.5, 30 \pm 15.5)$.

SIM_CODE_ISSUE: no