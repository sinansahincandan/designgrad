# Electronics enclosure base
The bottom half of an enclosure for an 80 x 50 mm circuit board.

## Coordinate system
Centred on the origin in X and Y; the outside of the floor is the plane z = 0; Z is up. The board sits horizontally with its
underside at z = 8.

## Requirements
- R1. One single, valid solid.
- R2. Floor: solid floor at least 2 mm thick (z from 0 to 2) under the whole board area.
- R3. Board space: the region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be completely free of material.
- R4. Walls: outer size 85 x 55 mm (+-1.5 mm) in X and Y; wall top at z between 30 and 32.5; continuous side walls on all four sides (except the cutout in R6).
- R5. Four screw bosses that support the board at (x, y) = (+-35, +-20): solid round bosses (outer diameter >= 6 mm) from the floor up to z = 8, each with a 2.2 mm pilot hole open at its top (hole at least 4 mm deep).
- R6. USB-C cutout through the -X wall: opening at least 9 mm wide (Y) and 3 mm high (Z), centred at y = 0, z = 14.
- R7. Mass <= 70 g.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
