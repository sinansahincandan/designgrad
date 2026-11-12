## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: PASS. Intersection volume shows floor covers almost the entire board area at $z=0$ to $2$.
- R3: PASS. Intersection volume with board space is 0.0, meaning it is empty.
- R4: PASS. Bounding box matches 85x55 and height 31 (within 30-32.5 range).
- R5: FAIL. Simulation check for bosses at $(\pm35, \pm20)$ shows `base_ok: false` and `od_ok: false`. The visual reviewer confirms bosses are not visible in renders, suggesting they failed to union or were not modeled. While the hole depth is okay, the boss structure itself fails.
- R6: UNSURE. Simulation was judged unfaithful/errored. Visual reviewer states the cutout is completely missing from the -X wall. Since I cannot rely on a failed simulation and the visual evidence shows it missing, but the requirement asks for a verdict based on evidence, I must note the contradiction. However, per instructions, if evidence cannot decide, say UNSURE.
- R7: PASS. Mass is ~45.6g, which is $\le 70$g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: PASS - Intersection volume shows floor exists at $z=0$ to $2$.
R3: PASS - Intersection volume with board space is 0.0.
R4: PASS - Bounding box is 85x55x31.
R5: FAIL - Simulation shows bosses have incorrect OD and base; visual evidence shows bosses are missing.
R6: UNSURE - Simulation check failed/was unfaithful; visual evidence shows cutout is missing.
R7: PASS - Mass is ~45.6g.

## Problems
- Screw Bosses (R5): Bosses are not visible in renders and simulation reports incorrect OD and base presence.
- USB-C Cutout (R6): Opening is completely missing from the -X wall.

SIM_CODE_ISSUE: yes