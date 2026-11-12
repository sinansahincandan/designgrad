# Drone arm
A printed arm that connects a small quadcopter frame to one motor.

## Coordinate system
The arm lies along +X starting at x = 0 (frame side). Its underside is the plane z = 0; Z up. The motor sits on top at (x, y) = (120, 0).

## Requirements
- R1. One single, valid solid.
- R2. Envelope: minimum x = 0, maximum x <= 136, |y| <= 16, minimum z = 0, height <= 20 mm.
- R3. Frame attachment: two vertical holes, diameter 3.2 mm, at (x, y) = (6, +-6).
- R4. Motor mount: four vertical holes, diameter 3.2 mm, at (x, y) = (120 +- 8, +-9.5), and a 6 mm vertical clearance hole for the shaft at (120, 0) through the whole part.
- R5. Strength: motor thrust 12 N upward at x = 120. Using beam theory on the section cut by the plane x = 20 the bending stress must be <= 30 MPa.
- R6. Stiffness: tip deflection estimate F*L^3/(3*E*I) with L = 100 mm and I of the x = 20 section <= 1.0 mm.
- R7. Mass <= 20 g.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
