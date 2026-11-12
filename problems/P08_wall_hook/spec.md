# Wall hook for a bag strap
A screw-on wall hook that holds a bag by a 10 mm wide strap.

## Coordinate system
The wall is the plane x = 0; the hook is in x >= 0. Z up, Y horizontal along the wall.

## Requirements
- R1. One single, valid solid.
- R2. A flat back plate on the wall: solid material at 0 <= x <= 2 over |y| <= 8, -5 <= z <= 45; minimum x = 0.
- R3. Two screw holes, diameter 4.5 mm, along X through the back plate at (y, z) = (0, 0) and (0, 40); plate at least 4 mm thick around them.
- R4. Strap seat: the strap (10 mm wide, 6 mm thick) rests on a solid bed whose top is at z = -14 under 34 <= x <= 46, |y| <= 4, and the space just above it (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty.
- R5. Retaining lip: solid material at 47 <= x <= 52, |y| <= 4, -13 <= z <= -8 so the strap cannot slide off.
- R6. Strength: 50 N downward at x = 40. Using beam theory on the section cut by the plane x = 8: bending stress <= 25 MPa and tip deflection estimate F*L^3/(3*E*I) with L = 32 mm <= 1.5 mm.
- R7. Mass <= 25 g; X extent <= 55 mm.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
