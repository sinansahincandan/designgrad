# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 9 | 3.22 | [2.22, 4.22] | 1 | 3.22 | 3 | 1.7 | 2/9 |
| L1 | 9 | 3.44 | [2.56, 4.33] | 1 | 3.89 | 24 | 8.3 | 7/35 |
| L2 | 9 | 4.11 | [3.33, 5.00] | 1 | 4.33 | 44 | 17.6 | 14/90 |
| L3 | 9 | 4.44 | [3.56, 5.22] | 2 | 4.56 | 45 | 17.1 | 9/90 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | +0.22 | [-0.78, +1.00] | 3/5/1 |
| L1->L2 | +0.67 | [+0.00, +1.44] | 4/4/1 |
| L2->L3 | +0.33 | [-0.56, +1.22] | 3/4/2 |
| L0->L2 | +0.89 | [+0.44, +1.33] | 6/3/0 |
| L0->L3 | +1.22 | [+0.44, +2.00] | 5/4/0 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 15/93 | 37/88 | 8/18 | 3/4 | [3.44, 3.67, 3.67, 3.78, 3.44] |
| L2 | 21/111 | 49/133 | 8/28 | 5/8 | [3.44, 3.67, 3.78, 3.89, 4.11] |
| L3 | 22/104 | 36/140 | 10/26 | 5/6 | [3.44, 3.89, 4.0, 4.22, 4.44] |

L2: own analysis agrees with the tests in 0.919 of 246 checks; of 113 unmet requirement-rounds it had flagged 102.

L3: own analysis agrees with the tests in 0.926 of 258 checks; of 113 unmet requirement-rounds it had flagged 102.

L2 analysis entries: agree 226, false alarm 12, missed 8, disputed 0, unmeasured 3; unmet requirement-rounds 113, reported as not met 102.

L3 analysis entries: agree 239, false alarm 14, missed 5, disputed 2, unmeasured 10; unmet requirement-rounds 113, reported as not met 102.

L3: 70 render complaints name a requirement; 14 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P02_phone_stand@s0 | 2 | 3 | 3 | 5 |
| P02_phone_stand@s1000 | 4 | 1 | 4 | 4 |
| P05_pipe_clamp@s0 | 3 | 3 | 4 | 3 |
| P05_pipe_clamp@s1000 | 2 | 4 | 3 | 5 |
| P06_heat_sink@s0 | 6 | 6 | 6 | 6 |
| P06_heat_sink@s1000 | 4 | 4 | 4 | 6 |
| P09_drone_arm@s0 | 4 | 4 | 5 | 5 |
| P09_drone_arm@s1000 | 4 | 4 | 6 | 4 |
| P10_sensor_tilt_mount@s0 | 0 | 2 | 2 | 2 |
