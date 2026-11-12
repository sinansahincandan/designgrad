## Working
- R1: PASS. Simulation confirms 1 solid in STEP file.
- R2: FAIL. Measured x_ext = 100.47 mm, which exceeds the 100 mm limit. Height (111.43 mm) and z_min (0.0) are within limits.
- R3: FAIL. Point-in-mesh sampling found 226 points of intersection with the phone volume.
- R4: PASS. Volume fraction sampling confirms material exists in the specified region.
- R5: PASS. Volume fraction sampling confirms seat and lip regions are occupied.
- R6: PASS. Combined COM x-projection is -24.58. Footprint x-range is [-50.47, 50.0]. The distance from -24.58 to the nearest edge (-50.47) is ~25.89 mm, which is > 5 mm margin.
- R7: FAIL. Measured mass is 64.98 g, exceeding the 60 g limit.

## Verdicts
R1: PASS - Counted 1 solid in STEP file.
R2: FAIL - x_ext is 100.47 mm, exceeding 100 mm limit.
R3: FAIL - 226 points of intersection detected with phone volume.
R4: PASS - Material present in specified region.
R5: PASS - Material present in seat and lip regions.
R6: PASS - Combined COM projects into footprint with > 5mm margin.
R7: FAIL - Mass is 64.98 g, exceeding 60 g limit.

## Problems
- R3: Phone intersection - 226 points of interference detected.
- R7: Mass - 64.98 g (limit 60 g).
- R2: Footprint width - x_ext is 100.47 mm (limit 100 mm).

SIM_CODE_ISSUE: no