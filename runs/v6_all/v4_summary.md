# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 9 | 4.00 | [2.89, 5.22] | 1 | 4.00 | 2 | 1.1 | 1/9 |
| L1 | 9 | 4.22 | [3.11, 5.44] | 1 | 5.00 | 14 | 4.4 | 1/28 |
| L2 | 9 | 4.89 | [4.00, 5.78] | 1 | 5.11 | 39 | 14.1 | 2/90 |
| L3 | 9 | 5.11 | [4.33, 5.89] | 1 | 5.67 | 44 | 15.4 | 2/90 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | +0.22 | [-0.67, +1.33] | 2/5/2 |
| L1->L2 | +0.67 | [-0.33, +1.78] | 3/5/1 |
| L2->L3 | +0.22 | [-0.56, +1.11] | 2/6/1 |
| L0->L2 | +0.89 | [+0.33, +1.44] | 5/4/0 |
| L0->L3 | +1.11 | [+0.44, +1.89] | 5/4/0 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 11/71 | 8/62 | 8/11 | 2/5 | [4.22, 4.44, 4.11, 4.11, 4.22] |
| L2 | 11/90 | 14/162 | 8/28 | 5/7 | [4.22, 4.44, 4.56, 4.78, 4.89] |
| L3 | 25/79 | 17/173 | 6/30 | 5/12 | [4.22, 4.78, 5.11, 5.11, 5.11] |

L2: own analysis agrees with the tests in 0.947 of 304 checks; of 111 unmet requirement-rounds it had flagged 106.

L3: own analysis agrees with the tests in 0.856 of 313 checks; of 96 unmet requirement-rounds it had flagged 93.

L2 analysis entries: agree 288, false alarm 13, missed 3, disputed 4, unmeasured 0; unmet requirement-rounds 111, reported as not met 107.

L3 analysis entries: agree 268, false alarm 43, missed 2, disputed 2, unmeasured 0; unmet requirement-rounds 96, reported as not met 94.

L3: 103 render complaints name a requirement; 27 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P01_shelf_bracket@s0 | 3 | 3 | 4 | 4 |
| P01_shelf_bracket@s1000 | 3 | 4 | 4 | 5 |
| P01_shelf_bracket@s2000 | 4 | 3 | 6 | 4 |
| P03_enclosure_base@s0 | 7 | 7 | 7 | 7 |
| P03_enclosure_base@s1000 | 6 | 6 | 6 | 6 |
| P03_enclosure_base@s2000 | 6 | 6 | 6 | 6 |
| P07_nema17_mount@s0 | 3 | 3 | 3 | 6 |
| P07_nema17_mount@s1000 | 3 | 1 | 5 | 5 |
| P07_nema17_mount@s2000 | 1 | 5 | 3 | 3 |
