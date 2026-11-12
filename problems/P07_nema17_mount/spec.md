# NEMA 17 motor mount
An L-shaped bracket that holds a NEMA 17 stepper motor against a vertical face plate and screws down to a table.

## Coordinate system
The table is z = 0, Z up. The motor's mounting face presses against the plane y = 0 from the -Y side; the motor body
(42.3 mm square, 48 mm long) lies in y < 0 with its shaft axis along Y through (x = 0, z = 30). The bracket is on the +Y side.

## Requirements
- R1. One single, valid solid.
- R2. Face plate at least 4 mm thick (y = 0 to 4) with solid material all around the central bore.
- R3. Central bore diameter 22.5 mm through the face plate, on the shaft axis.
- R4. Four motor screw holes, diameter 3.4 mm, through the face plate along Y at (x, z) = (+-15.5, 30 +- 15.5).
- R5. Motor clearance: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5.
- R6. Base on the table (minimum z = 0) with two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25).
- R7. Envelope -35 <= x <= 35, top <= 55 mm; mass <= 60 g.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
