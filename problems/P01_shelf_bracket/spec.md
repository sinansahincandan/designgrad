# Shelf bracket
A wall-mounted bracket that carries the end of a shelf.

## Coordinate system
The wall is the plane x = 0; the bracket lies in x >= 0 and touches the wall. Z is up. Y is along the wall (horizontal).

## Requirements
- R1. One single, valid solid.
- R2. Envelope: the part fits inside 0 <= x <= 170, -20 <= y <= 20, 0 <= z <= 130 and touches the wall (minimum x = 0).
- R3. Two screw holes, diameter 5.5 mm, axis along X, through the part where it sits on the wall, centred at (y=0, z=20) and (y=0, z=60). A screwdriver must reach each screw head from the front: no material within 4 mm of either hole axis for x >= 10.
- R4. Shelf support: the shelf rests on a horizontal top surface at exactly z = 110 that reaches at least x = 150 (solid material directly below z = 110 between x = 140 and 150 around y = 0). Nothing of the bracket may be above z = 110 for x >= 8.
- R5. Strength: a downward load of 150 N acts at x = 150. Using cantilever beam theory on the cross-section cut by the plane x = 10, the bending stress M*c/I must be <= 20 MPa (M = 150 N x 140 mm).
- R6. Stiffness: estimated tip deflection F*L^3/(3*E*I) with L = 140 mm and I of the x = 10 section must be <= 2.0 mm.
- R7. Mass <= 90 g.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
