import math
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Trsf, gp_Ax1
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge2d, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform,
                                     BRepBuilderAPI_MakeEdge)
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Extend.ShapeFactory import make_wire
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

centre_cylinder = BRepPrimAPI_MakeCylinder(1, 1).Shape()

total_boxes = 10

# Basic stator dimensions
active_length = 50
active_length_vec = gp_Vec(0, 0, active_length)
stator_inner_radius = 80
stator_outer_radius = 160
slot_opening_depth = 2
slot_opening_width = "N/A"

stator_inner = BRepPrimAPI_MakeCylinder(stator_inner_radius, active_length).Shape()
stator_outer = BRepPrimAPI_MakeCylinder(stator_outer_radius, active_length).Shape()
stator = BRepAlgoAPI_Cut(stator_outer, stator_inner).Shape()

# Basic slot dimensions
slot_depth = 50
slot_top_radius = stator_inner_radius + slot_opening_depth
slot_base_radius = slot_top_radius + slot_depth
width_slot_top = 15
width_slot_base = (slot_base_radius / slot_top_radius) * width_slot_top
slot_top_angle = math.radians(360 * (0.5 * width_slot_top / (2 * math.pi * slot_top_radius)))
slot_base_angle = math.radians(360 * (0.5 * width_slot_base / (2 * math.pi * slot_base_radius)))

# Defining the points
p1 = gp_Pnt2d(math.cos(slot_top_angle) * slot_top_radius,
              math.sin(slot_top_angle) * slot_top_radius)
p2 = gp_Pnt2d(math.cos(slot_top_angle) * slot_top_radius,
              -(math.sin(slot_top_angle) * slot_top_radius))
p3 = gp_Pnt2d(math.cos(slot_base_angle) * slot_base_radius,
              math.sin(slot_base_angle) * slot_base_radius)
p4 = gp_Pnt2d(math.cos(slot_base_angle) * slot_base_radius,
              -(math.sin(slot_base_angle) * slot_base_radius))
pt = gp_Pnt2d(slot_top_radius, 0)
pb = gp_Pnt2d(slot_base_radius, 0)

# Defining the edges
arc_top = GCE2d_MakeArcOfCircle(p1, pt, p2).Value()
arc_base = GCE2d_MakeArcOfCircle(p3, pb, p4).Value()
edge_top = BRepBuilderAPI_MakeEdge2d(arc_top).Edge()
edge_base = BRepBuilderAPI_MakeEdge2d(arc_base).Edge()
edge_left = BRepBuilderAPI_MakeEdge2d(p2, p4).Edge()
edge_right = BRepBuilderAPI_MakeEdge2d(p1, p3).Edge()

# Combine edges into a wire
slot_wire = BRepBuilderAPI_MakeWire(edge_top, edge_left, edge_base, edge_right).Wire()

# Turn into a face
slot_face = BRepBuilderAPI_MakeFace(slot_wire).Face()

# Extrude the face
slot = BRepPrimAPI_MakePrism(slot_face, active_length_vec, False, True)
slot.Build()
slot = slot.Shape()

# Transformation
trns = gp_Trsf()
rot = gp_Trsf()

num_of_box = 0
while num_of_box < total_boxes:

    radians = num_of_box*((2*math.pi)/total_boxes)

    rot.SetRotation(gp_Ax1(), radians)

    slot_rot = BRepBuilderAPI_Transform(slot, rot, False)
    slot_rot.Build()
    slot_rot = slot_rot.Shape()

    if radians == 0:
        fused_slot = BRepAlgoAPI_Fuse(slot, slot_rot).Shape()
    else:
        fused_slot = BRepAlgoAPI_Fuse(fused_slot, slot_rot).Shape()

    num_of_box += 1

stator = BRepAlgoAPI_Cut(stator, fused_slot).Shape()

# Display shape
display.DisplayShape(centre_cylinder, update=True)
display.DisplayShape(stator, update=True)
# display.DisplayShape(fused_slot, update=True)

start_display()
