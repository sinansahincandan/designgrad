# Ladder v4: requirements met (independent tests)

| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |
|---|---|---|---|---|---|---|---|---|
| L0 | 1 | 6.00 | [6.00, 6.00] | 0 | 6.00 | 1 | 0.8 | 0/1 |
| L1 | 1 | 5.00 | [5.00, 5.00] | 0 | 6.00 | 24 | 6.1 | 0/5 |
| L2 | 1 | 6.00 | [6.00, 6.00] | 0 | 6.00 | 33 | 11.3 | 0/10 |
| L3 | 1 | 5.00 | [5.00, 5.00] | 0 | 6.00 | 54 | 21.9 | 0/10 |

| Step | Mean | 95% CI | W/T/L |
|---|---|---|---|
| L0->L1 | -1.00 | [-1.00, -1.00] | 0/0/1 |
| L1->L2 | +1.00 | [+1.00, +1.00] | 1/0/0 |
| L2->L3 | -1.00 | [-1.00, -1.00] | 0/0/1 |
| L0->L2 | +0.00 | [+0.00, +0.00] | 0/1/0 |
| L0->L3 | -1.00 | [-1.00, -1.00] | 0/0/1 |

| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |
|---|---|---|---|---|---|
| L1 | 1/7 | 3/21 | 1/3 | 0/0 | [6.0, 5.0, 5.0, 5.0, 5.0] |
| L2 | 0/4 | 4/24 | 0/4 | 0/0 | [6.0, 6.0, 6.0, 6.0, 6.0] |
| L3 | 0/4 | 2/24 | 1/3 | 0/0 | [6.0, 6.0, 6.0, 6.0, 5.0] |

L2: own analysis agrees with the tests in 0.971 of 35 checks; of 9 unmet requirement-rounds it had flagged 8.

L3: own analysis agrees with the tests in 0.970 of 33 checks; of 7 unmet requirement-rounds it had flagged 4.

L3: 13 render complaints name a requirement; 2 of them are about requirements that are met.

| Unit | L0 | L1 | L2 | L3 |
|---|---|---|---|---|
| P08_wall_hook@v4pilot | 6 | 5 | 6 | 5 |
