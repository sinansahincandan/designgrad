## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection check shows floor exists from z=0 to z=2 under the board area.
- R3: PASS. Intersection check shows zero material in the specified cavity volume.
- R4: PASS. Bounding box measurements (85x55, zmax=31) match requirements.
- R5: FAIL. The design document states bosses extend from $z=2$ to $z=8$. However, the pilot hole is defined as being from $z=4$ to $z=8$. This makes the hole 4mm deep, which meets the "at least 4mm" requirement. But R5 also requires the boss to be a solid round boss from the floor ($z=0$) up to $z=8$. If the pilot hole starts at $z=4$, there is material from $z=2$ to $z=4$ that is not part of the "hole". However, looking at the simulation failure: the reviewer notes the probe checks $z=4$ to $8$. The design says the boss goes from $z=2$ to $z=8$. If the hole is 4mm deep (from $z=4$ to $z=8$), it satisfies R5. But wait, the requirement says "each with a 2.2 mm pilot hole open at its top". If the boss is from $z=2$ to $z=8$, and the hole is from $z=4$ to $z=8$, the hole is indeed 4mm deep and open at the top. However, the simulation failed R5. Looking closer: The design says "Bosses extend strictly from the top of the floor (z=2) to the bottom of the board cavity (z=8)". If they start at $z=2$, they are not "from the floor" ($z=0$). R5 requires bosses "from the floor up to z = 8".
- R6: FAIL. The simulation reports `empty_ratio: 0.0` for the cutout void, meaning no material was removed (the hole is not there). Even though the design document claims a cutout exists, the measured evidence shows it failed to create the void.
- R7: PASS. Mass is ~31.86g, which is $\le$ 70g.

## Verdicts
R1: PASS - Measured 1 solid.
R2: PASS - Floor thickness and coverage verified.
R3: PASS - Cavity volume is empty.
R4: PASS - Dimensions 85x55x31 match requirements.
R5: FAIL - Bosses start at z=2, but requirement R5 requires them to go from the floor (z=0).
R6: FAIL - Simulation shows empty_ratio of 0.0, meaning no cutout void was created.
R7: PASS - Mass is ~31.86g.

## Problems
- USB-C Cutout: The cutout at $x=-42.5$ has no void (empty_ratio 0.0). It must have a 9mm (Y) x 3mm (Z) opening.
- Screw Bosses: Bosses start at z=2, but must extend from the floor (z=0).

SIM_CODE_ISSUE: no