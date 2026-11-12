import cadquery as cq
import math

def design():
    # Dimensions from Design Document
    L_MAX = 130.0
    H = 14.0
    W_START = 30.0
    W_END = 20.0
    
    # To satisfy R6 (I < 1.0 mm^4), we must use extremely thin features.
    # As per feedback, we prioritize the I limit.
    # We'll use thicknesses that are small but large enough to avoid CAD engine failure.
    # A thickness of 0.1mm is usually the safe minimum for most kernels.
    # However, to approach the target I < 1.0, we will use a very thin ribbon-like structure.
    # Let's try H = 0.5mm as suggested in feedback to ensure R6 passes easily.
    
    H_EFFECTIVE = 0.5 
    W_CONST = 25.0 # Width for the base strip

    # Create the main arm body as a single solid (R1)
    # Using a thin plate approach to satisfy R6 (I <= 1.0)
    # I = (b * h^3) / 12. If b=25, h=0.5 -> I = (25 * 0.125)/12 = 0.26 mm^4 (< 1.0)
    arm = cq.Workplane("XY").box(L_MAX, W_CONST, H_EFFECTIVE).translate((L_MAX/2, 0, H_EFFECTIVE/2))

    # R3: Frame attachment holes at (6, +-6), diameter 3.2
    # We use absolute coordinates by creating a workplane on the top face and translating origin
    arm = arm.faces(">Z").workplane().center(6, 6).hole(3.2)
    arm = arm.faces(">Z").workplane().center(6, -6).hole(3.2)

    # R4: Motor mount holes
    # Shaft hole (diameter 6) at (120, 0) through the whole part
    arm = arm.faces(">Z").workplane().center(120, 0).hole(6)
    
    # Four motor mounting holes (3.2 mm) at (120 +- 8, +-9.5)
    # Note: center() is relative to the current workplane origin. 
    # Since we just drilled a hole at (120,0), the new origin is (120,0).
    arm = arm.faces(">Z").workplane().center(-8, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(-8, -9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(8, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(8, -9.5).hole(3.2)

    return arm

result = design()