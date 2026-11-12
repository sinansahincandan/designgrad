# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 3 | 4.33 | [3.00, 7.00] | 1 | 4.33 | 1 | 0.5 | 0/3 |
| L1 | 3 | 4.00 | [2.00, 7.00] | 1 | 4.67 | 26 | 7.4 | 1/15 |
| L2 | 3 | 5.67 | [3.00, 7.00] | 2 | 6.00 | 45 | 17.5 | 0/30 |
| L3 | 3 | 6.00 | [4.00, 7.00] | 2 | 6.33 | 48 | 18.0 | 0/30 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | -0.33 | [-1.00, +0.00] | 0/2/1 |
| L1->L2 | +1.67 | [+0.00, +5.00] | 1/2/0 |
| L2->L3 | +0.33 | [-3.00, +4.00] | 1/1/1 |
| L0->L2 | +1.33 | [+0.00, +4.00] | 1/2/0 |
| L0->L3 | +1.67 | [+0.00, +4.00] | 2/1/0 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 4/35 | 5/49 | 2/10 | 0/1 | [4.33, 4.0, 4.0, 4.0, 4.0] |
| L2 | 6/22 | 3/62 | 3/9 | 2/4 | [4.33, 5.33, 5.33, 5.67, 5.67] |
| L3 | 6/18 | 8/66 | 3/9 | 3/4 | [4.33, 5.67, 6.0, 6.0, 6.0] |

L2: own analysis agrees with the tests in 0.790 of 100 checks; of 27 unmet requirement-rounds it had flagged 14.

L3: own analysis agrees with the tests in 0.914 of 93 checks; of 28 unmet requirement-rounds it had flagged 18.

L3: 33 render complaints name a requirement; 16 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P01_shelf_bracket@s0 | 3 | 2 | 7 | 4 |
| P03_enclosure_base@s0 | 7 | 7 | 7 | 7 |
| P07_nema17_mount@s0 | 3 | 3 | 3 | 7 |
