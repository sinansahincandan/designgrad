# Desk phone stand
A one-piece desk stand that holds a phone leaning back for video calls.

## The phone (fixed, do not model it)
Phone: 160 x 75 x 9 mm, 200 g. Its bottom-back edge lies along the Y axis line at (x = 0, z = 8), from y = -37.5 to 37.5.
The phone leans back toward -X at 65 degrees from horizontal: its long axis is u = (-cos65, 0, sin65) and its screen faces
n = (sin65, 0, cos65). The phone occupies every point (0, y, 8) + a*u + b*n with 0 <= a <= 160, 0 <= b <= 9, |y| <= 37.5.
Its centre of mass is at (0, 0, 8) + 80*u + 4.5*n.

## Requirements
- R1. One single, valid solid.
- R2. Stands on the desk plane z = 0 (minimum z = 0). Footprint within 100 x 100 mm (x and y extents), height <= 120 mm.
- R3. The stand must not intersect the phone volume.
- R4. Back support: material directly behind the phone back (within 2 mm, -2 <= b <= 0) somewhere between a = 90 and a = 110 near the middle (|y| <= 15).
- R5. Seat and lip: material just below the phone's bottom edge (-4 <= a <= 0, 0 <= b <= 9, |y| <= 15) so it cannot slide down, and a front lip (0 <= a <= 8, 9 <= b <= 13, |y| <= 15) so the bottom cannot slide forward.
- R6. Stability: the combined centre of mass of stand + phone must project inside the stand's contact area on the desk with at least 5 mm margin.
- R7. Mass <= 60 g.

## Material
PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa.

## Output
Write CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) to a variable named `result`.
