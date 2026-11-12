# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 3 | 4.33 | [3.00, 7.00] | 1 | 4.33 | 1 | 0.5 | 0/3 |
| L1 | 3 | 4.33 | [3.00, 7.00] | 1 | 4.67 | 15 | 4.9 | 0/10 |
| L2 | 3 | 6.33 | [6.00, 7.00] | 1 | 6.67 | 53 | 23.9 | 0/30 |
| L3 | 3 | 5.67 | [4.00, 7.00] | 1 | 5.67 | 57 | 26.9 | 0/30 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | +0.00 | [+0.00, +0.00] | 0/3/0 |
| L1->L2 | +2.00 | [+0.00, +3.00] | 2/1/0 |
| L2->L3 | -0.67 | [-2.00, +0.00] | 0/2/1 |
| L0->L2 | +2.00 | [+0.00, +3.00] | 2/1/0 |
| L0->L3 | +1.33 | [+0.00, +3.00] | 2/1/0 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 1/28 | 0/21 | 2/5 | 0/1 | [4.33, 4.33, 4.33, 4.33, 4.33] |
| L2 | 8/14 | 12/70 | 2/10 | 2/3 | [4.33, 6.33, 6.33, 6.33, 6.33] |
| L3 | 5/22 | 4/62 | 4/8 | 2/2 | [4.33, 5.33, 5.33, 5.67, 5.67] |

L2: own analysis agrees with the tests in 0.920 of 87 checks; of 26 unmet requirement-rounds it had flagged 13.

L3: own analysis agrees with the tests in 0.864 of 88 checks; of 29 unmet requirement-rounds it had flagged 14.

L3: 29 render complaints name a requirement; 10 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P01_shelf_bracket@s0 | 3 | 3 | 6 | 6 |
| P03_enclosure_base@s0 | 7 | 7 | 7 | 7 |
| P07_nema17_mount@s0 | 3 | 3 | 6 | 4 |
