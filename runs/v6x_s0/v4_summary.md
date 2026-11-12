# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 5 | 3.00 | [1.20, 4.80] | 1 | 3.00 | 3 | 1.7 | 1/5 |
| L1 | 5 | 3.60 | [2.60, 4.80] | 1 | 3.80 | 24 | 8.7 | 4/19 |
| L2 | 5 | 4.00 | [2.80, 5.20] | 1 | 4.20 | 43 | 17.3 | 8/50 |
| L3 | 5 | 4.20 | [3.00, 5.40] | 1 | 4.20 | 43 | 15.6 | 6/50 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | +0.60 | [+0.00, +1.40] | 2/3/0 |
| L1->L2 | +0.40 | [+0.00, +0.80] | 2/3/0 |
| L2->L3 | +0.20 | [-0.60, +1.20] | 1/3/1 |
| L0->L2 | +1.00 | [+0.40, +1.60] | 4/1/0 |
| L0->L3 | +1.20 | [+0.20, +2.20] | 3/2/0 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 5/53 | 13/44 | 5/9 | 1/2 | [3.4, 3.6, 3.6, 3.6, 3.6] |
| L2 | 7/61 | 25/75 | 4/16 | 3/5 | [3.4, 3.8, 3.8, 4.0, 4.0] |
| L3 | 6/56 | 20/80 | 3/17 | 2/2 | [3.4, 4.2, 4.2, 4.2, 4.2] |

L2: own analysis agrees with the tests in 0.894 of 132 checks; of 61 unmet requirement-rounds it had flagged 52.

L3: own analysis agrees with the tests in 0.924 of 132 checks; of 52 unmet requirement-rounds it had flagged 45.

L2 analysis entries: agree 118, false alarm 8, missed 6, disputed 0, unmeasured 3; unmet requirement-rounds 61, reported as not met 52.

L3 analysis entries: agree 122, false alarm 6, missed 4, disputed 0, unmeasured 3; unmet requirement-rounds 52, reported as not met 45.

L3: 33 render complaints name a requirement; 9 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P02_phone_stand@s0 | 2 | 3 | 3 | 5 |
| P05_pipe_clamp@s0 | 3 | 3 | 4 | 3 |
| P06_heat_sink@s0 | 6 | 6 | 6 | 6 |
| P09_drone_arm@s0 | 4 | 4 | 5 | 5 |
| P10_sensor_tilt_mount@s0 | 0 | 2 | 2 | 2 |
