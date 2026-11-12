# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 3 | 4.33 | [3.00, 7.00] | 1 | 4.33 | 1 | 0.5 | 0/3 |
| L1 | 3 | 4.33 | [3.00, 7.00] | 1 | 4.67 | 15 | 4.9 | 0/10 |
| L2 | 3 | 4.67 | [3.00, 7.00] | 1 | 4.67 | 39 | 14.0 | 1/30 |
| L3 | 3 | 5.67 | [4.00, 7.00] | 1 | 6.00 | 42 | 14.4 | 1/30 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | +0.00 | [+0.00, +0.00] | 0/3/0 |
| L1->L2 | +0.33 | [+0.00, +1.00] | 1/2/0 |
| L2->L3 | +1.00 | [+0.00, +3.00] | 1/2/0 |
| L0->L2 | +0.33 | [+0.00, +1.00] | 1/2/0 |
| L0->L3 | +1.33 | [+0.00, +3.00] | 2/1/0 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 1/28 | 0/21 | 2/5 | 0/1 | [4.33, 4.33, 4.33, 4.33, 4.33] |
| L2 | 1/31 | 5/53 | 2/10 | 1/1 | [4.33, 4.33, 4.33, 4.67, 4.67] |
| L3 | 8/20 | 9/64 | 3/9 | 2/3 | [4.33, 5.67, 5.67, 5.67, 5.67] |

L2: own analysis agrees with the tests in 0.918 of 97 checks; of 36 unmet requirement-rounds it had flagged 36.

L3: own analysis agrees with the tests in 0.875 of 104 checks; of 29 unmet requirement-rounds it had flagged 29.

L2 analysis entries: agree 89, false alarm 8, missed 0, disputed 1, unmeasured 0; unmet requirement-rounds 36, reported as not met 36.

L3 analysis entries: agree 91, false alarm 13, missed 0, disputed 1, unmeasured 0; unmet requirement-rounds 29, reported as not met 29.

L3: 38 render complaints name a requirement; 12 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P01_shelf_bracket@s0 | 3 | 3 | 4 | 4 |
| P03_enclosure_base@s0 | 7 | 7 | 7 | 7 |
| P07_nema17_mount@s0 | 3 | 3 | 3 | 6 |
