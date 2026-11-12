# Tilted sensor mount
A desk mount that holds a 50 g sensor board facing forward and tilted up by 30 degrees.

## Coordinate system
The desk is z = 0, Z up. "Forward" is +Y.

## Requirements
- R1. One single, valid solid.
- R2. Base on the desk (minimum z = 0) with two vertical screw holes, diameter 4.5 mm, at (x, y) = (+-20, -10).
- R3. Mounting face: one flat face of at least 900 mm2 whose outward normal is n = (0, cos30, sin30) (facing forward, tilted up 30 deg).
- R4. The centre of that face is at a height between 35 and 50 mm.
- R5. Two sensor screw holes, diameter 3.2 mm, perpendicular to the mounting face, at the face centre +- 10 mm along X.
- R6. Stability: with the 50 g sensor (its centre of mass 15 mm in front of the face centre, along n) the combined centre of mass must lie inside the contact area with >= 5 mm margin.
- R7. Mass <= 35 g.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
