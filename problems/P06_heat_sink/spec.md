# Passive heat sink
A finned aluminium heat sink for a 40 x 40 mm chip, cooled by natural convection.

## Coordinate system
The base's underside (chip contact) is the plane z = 0, centred on the origin in X and Y; Z up.

## Requirements
- R1. One single, valid solid.
- R2. Footprint exactly 40 x 40 mm (+-0.5), centred on the origin; total height <= 25 mm.
- R3. Solid base at least 3 mm thick (z = 0 to 3) over the whole footprint.
- R4. Thermal: natural-convection resistance estimate R = 1 / (h * A * eta) with h = 10 W/(m2 K), eta = 0.85 and A the total surface area of the part must be <= 9 K/W.
- R5. Two mounting holes, diameter 3.2 mm, vertical through the base at (x, y) = (+-15, 0). A screwdriver must reach each screw from above: no material within 3 mm of either hole axis above the base (z >= 3).
- R6. Mass <= 45 g.

## Material
Aluminium 6063: density 2.70 g/cm3.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
