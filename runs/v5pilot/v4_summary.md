# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 1 | 6.00 | [6.00, 6.00] | 0 | 6.00 | 1 | 0.6 | 0/1 |
| L1 | 1 | 4.00 | [4.00, 4.00] | 0 | 6.00 | 17 | 8.4 | 1/3 |
| L2 | 1 | 6.00 | [6.00, 6.00] | 0 | 7.00 | 47 | 21.9 | 0/10 |
| L3 | 1 | 5.00 | [5.00, 5.00] | 0 | 6.00 | 63 | 29.3 | 1/10 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | -2.00 | [-2.00, -2.00] | 0/0/1 |
| L1->L2 | +2.00 | [+2.00, +2.00] | 1/0/0 |
| L2->L3 | -1.00 | [-1.00, -1.00] | 0/0/1 |
| L0->L2 | +0.00 | [+0.00, +0.00] | 0/1/0 |
| L0->L3 | -1.00 | [-1.00, -1.00] | 0/0/1 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 0/2 | 4/12 | 1/1 | 0/0 | [6.0, 6.0, 4.0] |
| L2 | 1/4 | 1/24 | 0/4 | 0/1 | [6.0, 6.0, 6.0, 6.0, 6.0] |
| L3 | 0/6 | 3/22 | 1/3 | 0/0 | [6.0, 6.0, 5.0, 5.0, 5.0] |

L2: own analysis agrees with the tests in 0.941 of 34 checks; of 5 unmet requirement-rounds it had flagged 4.

L3: own analysis agrees with the tests in 0.970 of 33 checks; of 10 unmet requirement-rounds it had flagged 7.

L3: 15 render complaints name a requirement; 2 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P08_wall_hook@v5pilot | 6 | 4 | 6 | 5 |
