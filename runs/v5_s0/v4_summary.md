# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 3 | 4.33 | [3.00, 7.00] | 1 | 4.33 | 1 | 0.5 | 0/3 |
| L1 | 3 | 4.33 | [3.00, 7.00] | 1 | 4.67 | 15 | 4.9 | 0/10 |
| L2 | 3 | 5.00 | [3.00, 6.00] | 0 | 6.33 | 54 | 25.1 | 0/30 |
| L3 | 3 | 5.33 | [3.00, 7.00] | 1 | 6.67 | 59 | 26.9 | 1/30 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | +0.00 | [+0.00, +0.00] | 0/3/0 |
| L1->L2 | +0.67 | [-1.00, +3.00] | 1/1/1 |
| L2->L3 | +0.33 | [-3.00, +3.00] | 2/0/1 |
| L0->L2 | +0.67 | [-1.00, +3.00] | 1/1/1 |
| L0->L3 | +1.00 | [+0.00, +3.00] | 1/2/0 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 1/28 | 0/21 | 2/5 | 0/1 | [4.33, 4.33, 4.33, 4.33, 4.33] |
| L2 | 7/28 | 1/56 | 4/8 | 2/5 | [4.33, 4.67, 4.67, 5.0, 5.0] |
| L3 | 10/23 | 5/61 | 4/8 | 1/3 | [4.33, 5.33, 5.33, 5.33, 5.33] |

L2: own analysis agrees with the tests in 0.965 of 86 checks; of 30 unmet requirement-rounds it had flagged 16.

L3: own analysis agrees with the tests in 0.898 of 88 checks; of 26 unmet requirement-rounds it had flagged 17.

L3: 25 render complaints name a requirement; 12 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P01_shelf_bracket@s0 | 3 | 3 | 6 | 3 |
| P03_enclosure_base@s0 | 7 | 7 | 6 | 7 |
| P07_nema17_mount@s0 | 3 | 3 | 3 | 6 |
