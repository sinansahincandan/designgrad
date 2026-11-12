# Test tube rack
A rack for ten 16 mm test tubes in two rows of five.

## Coordinate system
The rack stands on z = 0, Z up, centred on the origin in X and Y.

## Requirements
- R1. One single, valid solid.
- R2. Footprint within 140 x 80 mm; the top of the rack at z = 60 (+-2 mm).
- R3. Ten tube holes, diameter 17 mm, vertical, centred at x = -44, -22, 0, 22, 44 and y = -12.5, 12.5. Each hole must be clear from its top down to z = 10, with a ring of material around it at the top.
- R4. Each tube rests on a solid floor: material under every tube from z = 0 to 3 (within 4 mm of the hole axis).
- R5. Tipping: with all ten tubes in place (20 g each, centre of mass at z = 55 on each hole axis), the loaded rack must not tip before 20 degrees: atan(d / h) >= 20 deg, where d is the distance from the combined centre of mass to the nearest edge of the contact area and h its height.
- R6. Mass <= 150 g.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
