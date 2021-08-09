import math
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Trsf, gp_Ax1
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Display.SimpleGui import init_display
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopAbs import (TopAbs_EDGE)
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Edge
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge2d, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform,
                                     BRepBuilderAPI_MakeVertex)

display, start_display, add_menu, add_function_to_menu = init_display()

centre_cylinder = BRepPrimAPI_MakeCylinder(1, 1).Shape()

# Basic stator dimensions
active_length = 90
active_length_vec = gp_Vec(0, 0, active_length)
stator_inner_radius = 80
stator_outer_radius = 200

stator_inner = BRepPrimAPI_MakeCylinder(stator_inner_radius, active_length).Shape()
stator_outer = BRepPrimAPI_MakeCylinder(stator_outer_radius, active_length).Shape()
stator = BRepAlgoAPI_Cut(stator_outer, stator_inner).Shape()

# Basic slot dimensions
num_of_slots = 15
fillet_radius = 5
slot_opening_depth = 10
slot_depth = 70
slot_top_radius = stator_inner_radius + slot_opening_depth
slot_base_radius = slot_top_radius + slot_depth
slot_top_circumference = 2 * math.pi * slot_top_radius
slot_base_circumference = 2 * math.pi * slot_base_radius

teeth_width = 12  # Using teeth_width instead of slot top and base widths.
teeth_angle_top = 2 * math.asin(teeth_width / 2 / slot_top_radius)
teeth_angle_base = 2 * math.asin(teeth_width / 2 / slot_base_radius)

# Constant slot opening width throughout
slot_opening_width = 5
slot_opening_top_angle = math.asin(slot_opening_width / 2 / stator_inner_radius)
slot_opening_base_angle = math.asin(slot_opening_width / 2 / (stator_inner_radius + slot_opening_depth))

teeth_arclength_top = slot_top_circumference * (teeth_angle_top / math.radians(360))
teeth_arclength_base = slot_base_circumference * (teeth_angle_base / math.radians(360))
total_teeth_arclength_top = teeth_arclength_top * num_of_slots
total_teeth_arclength_base = teeth_arclength_base * num_of_slots

width_slot_top = (slot_top_circumference - total_teeth_arclength_top) / num_of_slots
width_slot_base = (slot_base_circumference - total_teeth_arclength_base) / num_of_slots
slot_top_angle = math.radians(360 * (0.5 * width_slot_top / (2 * math.pi * slot_top_radius)))
slot_base_angle = math.radians(360 * (0.5 * width_slot_base / (2 * math.pi * slot_base_radius)))

# Defining the points
p1 = gp_Pnt2d(math.cos(slot_top_angle) * slot_top_radius,
              math.sin(slot_top_angle) * slot_top_radius)
p2 = gp_Pnt2d(math.cos(slot_top_angle) * slot_top_radius,
              -(math.sin(slot_top_angle) * slot_top_radius))
pt = gp_Pnt2d(slot_top_radius, 0)

sp1 = gp_Pnt2d(math.cos(slot_opening_top_angle) * stator_inner_radius,
               math.sin(slot_opening_top_angle) * stator_inner_radius)
sp2 = gp_Pnt2d(math.cos(slot_opening_top_angle) * stator_inner_radius,
               -(math.sin(slot_opening_top_angle) * stator_inner_radius))
sp3 = gp_Pnt2d(math.cos(slot_opening_base_angle) * (stator_inner_radius + slot_opening_depth),
               math.sin(slot_opening_base_angle) * (stator_inner_radius + slot_opening_depth))
sp4 = gp_Pnt2d(math.cos(slot_opening_base_angle) * (stator_inner_radius + slot_opening_depth),
               -(math.sin(slot_opening_base_angle) * (stator_inner_radius + slot_opening_depth)))
spt = gp_Pnt2d(stator_inner_radius, 0)
spb = gp_Pnt2d(stator_inner_radius + slot_opening_depth, 0)

# Defining vertex for fillet
p1_pnt = gp_Pnt(math.cos(slot_top_angle) * slot_top_radius, math.sin(slot_top_angle) * slot_top_radius, 0)
p1_pnt_extrude = gp_Pnt(math.cos(slot_top_angle) * slot_top_radius,
                        math.sin(slot_top_angle) * slot_top_radius,
                        active_length)
p2_pnt = gp_Pnt(math.cos(slot_top_angle) * slot_top_radius, -(math.sin(slot_top_angle) * slot_top_radius), 0)
p2_pnt_extrude = gp_Pnt(math.cos(slot_top_angle) * slot_top_radius,
                        -(math.sin(slot_top_angle) * slot_top_radius),
                        active_length)
p3_pnt = gp_Pnt(math.cos(slot_base_angle) * slot_base_radius, math.sin(slot_base_angle) * slot_base_radius, 0)
p3_pnt_extrude = gp_Pnt(math.cos(slot_base_angle) * slot_base_radius,
                        math.sin(slot_base_angle) * slot_base_radius,
                        active_length)
p4_pnt = gp_Pnt(math.cos(slot_base_angle) * slot_base_radius, -(math.sin(slot_base_angle) * slot_base_radius), 0)
p4_pnt_extrude = gp_Pnt(math.cos(slot_base_angle) * slot_base_radius,
                        -(math.sin(slot_base_angle) * slot_base_radius),
                        active_length)
v1 = BRepBuilderAPI_MakeVertex(p1_pnt).Vertex()
v1_extrude = BRepBuilderAPI_MakeVertex(p1_pnt_extrude).Vertex()
v2 = BRepBuilderAPI_MakeVertex(p2_pnt).Vertex()
v2_extrude = BRepBuilderAPI_MakeVertex(p2_pnt_extrude).Vertex()
v3 = BRepBuilderAPI_MakeVertex(p3_pnt).Vertex()
v3_extrude = BRepBuilderAPI_MakeVertex(p3_pnt_extrude).Vertex()
v4 = BRepBuilderAPI_MakeVertex(p4_pnt).Vertex()
v4_extrude = BRepBuilderAPI_MakeVertex(p4_pnt_extrude).Vertex()

# Defining the edges
arc_top = GCE2d_MakeArcOfCircle(p1, pt, p2).Value()
edge_top = BRepBuilderAPI_MakeEdge2d(arc_top).Edge()
edge_left = BRepBuilderAPI_MakeEdge2d(v2, v4).Edge()
edge_right = BRepBuilderAPI_MakeEdge2d(v1, v3).Edge()
edge_base = BRepBuilderAPI_MakeEdge2d(v3, v4).Edge()

slot_opening_arc_top = GCE2d_MakeArcOfCircle(sp1, spt, sp2).Value()
slot_opening_arc_base = GCE2d_MakeArcOfCircle(sp3, spb, sp4).Value()
slot_opening_edge_top = BRepBuilderAPI_MakeEdge2d(slot_opening_arc_top).Edge()
slot_opening_edge_base = BRepBuilderAPI_MakeEdge2d(slot_opening_arc_base).Edge()
slot_opening_edge_left = BRepBuilderAPI_MakeEdge2d(sp2, sp4).Edge()
slot_opening_edge_right = BRepBuilderAPI_MakeEdge2d(sp1, sp3).Edge()

# Combine edges into a wire
slot_wire = BRepBuilderAPI_MakeWire(edge_top, edge_left, edge_base, edge_right).Wire()
slot_opening_wire = BRepBuilderAPI_MakeWire(slot_opening_edge_top, slot_opening_edge_left,
                                            slot_opening_edge_right, slot_opening_edge_base).Wire()

# Turn into a face
slot_face = BRepBuilderAPI_MakeFace(slot_wire, True).Face()
slot_opening_face = BRepBuilderAPI_MakeFace(slot_opening_wire, True).Face()

# Extrude the face
slot = BRepPrimAPI_MakePrism(slot_face, active_length_vec, False, True)
slot.Build()
slot = slot.Shape()

slot_opening = BRepPrimAPI_MakePrism(slot_opening_face, active_length_vec, False, True)
slot_opening.Build()
slot_opening = slot_opening.Shape()

# Find edge to fillet
fillets = BRepFilletAPI_MakeFillet(slot)
edges = TopExp_Explorer(slot, TopAbs_EDGE)
while edges.More():
    current_edge = edges.Current()
    shapeAnalysis_firstVertex = ShapeAnalysis_Edge().FirstVertex(current_edge)
    shapeAnalysis_lastVertex = ShapeAnalysis_Edge().LastVertex(current_edge)
    sA_firstVertex = BRep_Tool().Pnt(shapeAnalysis_firstVertex).Coord()
    sA_lastVertex = BRep_Tool().Pnt(shapeAnalysis_lastVertex).Coord()

    if sA_firstVertex == p3_pnt.Coord() and sA_lastVertex == p3_pnt_extrude.Coord():
        fillets.Add(fillet_radius, current_edge)
    elif sA_firstVertex == p4_pnt.Coord() and sA_lastVertex == p4_pnt_extrude.Coord():
        fillets.Add(fillet_radius, current_edge)

    edges.Next()

fillets.Build()
slot = fillets.Shape()

slot = BRepAlgoAPI_Fuse(slot_opening, slot).Shape()

# Transformation
trns = gp_Trsf()
rot = gp_Trsf()

num_of_box = 0
while num_of_box < num_of_slots:

    radians = num_of_box*((2*math.pi)/num_of_slots)

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

# display.DisplayShape(slot, update=True)

start_display()
