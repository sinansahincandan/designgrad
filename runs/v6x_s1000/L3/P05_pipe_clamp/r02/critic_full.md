## Working
- R1: PASS. Simulation confirms 1 solid.
- R2: FAIL. The design document claims Y-extent is 20 mm, but simulation shows Y=40.0 and Zmin=-3.0 (it does not sit on z=0).
- R3: PASS. Simulation confirms zero intersection with the pipe volume.
- R4: PASS. Sampling confirms material exists in the specified band.
- R5: FAIL. Simulation shows cylinder intersection check failed at (+-27, 0), and the visual reviewer notes they are misaligned/offset from y=0.
- R6: FAIL. Simulation sampling shows only 0.6 (60%) coverage in the required flange region; visual reviewer confirms flanges do not match specified dimensions.
- R7: PASS. Mass is calculated at ~14.6 g, which is $\le$ 25 g.

## Verdicts
R1: PASS - Simulation confirms 1 solid.
R2: FAIL - Y extent is 40 mm (req: 18-22 mm) and Zmin is -3.0 (req: sits on z=0).
R3: PASS - Intersection volume ratio is 0.0.
R4: PASS - Sampling confirms material in the specified band.
R5: FAIL - Simulation shows holes are not correctly placed/formed at (+-27, 0).
R6: FAIL - Sampling shows only 60% coverage of the required flange region.
R7: PASS - Mass is ~14.6 g (req: $\le$ 25 g).

## Problems
- Y Extent: Current value 40 mm; should be between 18 and 22 mm.
- Z Position: Current Zmin is -3.0; should sit on z = 0.
- Screw Holes: Centering at (x, y) = (+-27, 0) is not achieved.
- Flanges: Required material coverage in $|x| \in [18.5, 23], |y| \le 4, z \in [0, 3]$ is only 60%; should be 100%.

SIM_CODE_ISSUE: no