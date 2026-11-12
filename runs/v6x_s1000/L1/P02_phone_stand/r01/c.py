import cadquery as cq

# Design Dimensions based on Design Document and Feedback
# Base Plate (R2): x in [-40, 20], y in [-45, 45], z in [0, 5]
# Width = 60, Depth = 90, Height = 5. Center at (-10, 0, 2.5)
stand_base = cq.Workplane("XY").box(60, 90, 5).translate((-10, 0, 2.5))

# Back Support (R4): x in [-7, 0], y in [-15, 15], z in [5, 105]
# Width = 7, Depth = 30, Height = 100. Center at (-3.5, 0, 55)
back_support = cq.Workplane("XY").box(7, 30, 100).translate((-3.5, 0, 55))

# Seat (R5 - part 1): x in [-10, 2], y in [-15, 15], z in [5, 7]
# Width = 12, Depth = 30, Height = 2. Center at (-4, 0, 6)
seat = cq.Workplane("XY").box(12, 30, 2).translate((-4, 0, 6))

# Lip (R5 - part 2): x in [2, 10], y in [-15, 15], z in [5, 8]
# Width = 8, Depth = 30, Height = 3. Center at (6, 0, 6.5)
lip = cq.Workplane("XY").box(8, 30, 3).translate((6, 0, 6.5))

# Final assembly: Union all parts into one single solid (R1)
result = (
    stand_base
    .union(back_support)
    .union(seat)
    .union(lip)
)