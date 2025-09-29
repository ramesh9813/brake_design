# cylinder_to_step.py
# Requires: cadquery >= 2.1  (pip install cadquery)

import cadquery as cq
from cadquery import exporters

# ---- parameters (millimeters) ----
diameter = 20.0   # Ø of the cylinder
height   = 50.0   # cylinder height
centered = True   # center shape on the workplane

# ---- model ----
cyl = (
    cq.Workplane("XY", origin=(0, 0, 0))
    .circle(diameter / 2.0)
    .extrude(height, combine=True, clean=True, both=not centered)
)

# ---- export ----
exporters.export(cyl, "cylinder.step", exporters.ExportTypes.STEP)

print("Wrote cylinder.step")
