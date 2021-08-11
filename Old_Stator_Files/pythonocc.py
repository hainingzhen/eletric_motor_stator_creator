import math
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge,
                                     BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace)
from OCC.Core.BRepPrimAPI import (BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder,
                                  BRepPrimAPI_MakePrism)
from OCC.Core.gp import gp_Vec, gp_Trsf, gp_Ax1, gp_Pnt
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

trns = gp_Trsf()
rot = gp_Trsf()

trns.SetTranslation(gp_Vec(0-5, 100-25, 0))

box = BRepPrimAPI_MakeBox(10., 50., 20).Shape()
centre_cylinder = BRepPrimAPI_MakeCylinder(5., 5).Shape()
stator_outer = BRepPrimAPI_MakeCylinder(160, 20).Shape()
stator_inner = BRepPrimAPI_MakeCylinder(80, 20).Shape()

stator = BRepAlgoAPI_Cut(stator_outer, stator_inner).Shape()

box_trns = BRepBuilderAPI_Transform(box, trns, False)
box_trns.Build()
box_trns = box_trns.Shape()

# rot.SetRotation(gp_Ax1(), PI/2)
#
# box_rot = BRepBuilderAPI_Transform(box_trns, rot, False)
# box_rot.Build()
# box_rot = box_rot.Shape()

PI = math.pi
num_of_box = 0
total_boxes = 15

while num_of_box < total_boxes:

    radians = num_of_box*((2*PI)/total_boxes)

    rot.SetRotation(gp_Ax1(), radians)

    box_rot = BRepBuilderAPI_Transform(box_trns, rot, False)
    box_rot.Build()
    box_rot = box_rot.Shape()

    if radians == 0:
        fused_boxes = BRepAlgoAPI_Fuse(box_trns, box_rot).Shape()
    else:
        fused_boxes = BRepAlgoAPI_Fuse(fused_boxes, box_rot).Shape()

    num_of_box += 1

stator = BRepAlgoAPI_Cut(stator, fused_boxes).Shape()

display.DisplayShape(centre_cylinder, update=True)
display.DisplayShape(stator, update=True)
# display.DisplayShape(slot, update=True)

# shapeUpgrade = ShapeUpgrade_UnifySameDomain(fused_shp, False, True, False)
# shapeUpgrade.Build()
# fused_shp_upgrade = shapeUpgrade.Shape()

start_display()