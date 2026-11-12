# Pipe saddle clamp
A clamp that holds a 25 mm pipe against a flat surface, fixed with two screws.

## Coordinate system
The mounting surface is the plane z = 0; Z up. The pipe (outer diameter 25 mm) lies on that surface along the Y axis: its axis is the line x = 0, z = 12.5.

## Requirements
- R1. One single, valid solid.
- R2. Sits on z = 0; clamp width (Y extent) between 18 and 22 mm; total X extent <= 80 mm.
- R3. The pipe volume (radius 12.6 mm around its axis) must be free of material.
- R4. The clamp wraps over the top of the pipe: solid material in the band 12.7 to 15.5 mm from the pipe axis directly above the pipe (|x| <= 7).
- R5. Two screw holes, diameter 6.6 mm, vertical, centred at (x, y) = (+-27, 0), through flanges that lie on the surface.
- R6. Flanges at least 3 mm thick: solid from z = 0 to 3 for 18.5 <= |x| <= 23, |y| <= 4.
- R7. Mass <= 25 g.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
