from math import cos, sin, pi
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Trsf, gp_Ax1
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge2d, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform, )


class SlotsBuilder:

    def __init__(self, calcResult, input):
        self.input = input
        slot_top_angle = calcResult["slot_top_angle"]
        slot_base_angle = calcResult["slot_base_angle"]
        slot_top_radius = calcResult["slot_top_radius"]
        slot_base_radius = calcResult["slot_base_radius"]
        hyp_top = calcResult["hyp_top"]
        hyp_base = calcResult["hyp_base"]
        slot_opening_top_angle = calcResult["slot_opening_top_angle"]
        slot_opening_base_angle = calcResult["slot_opening_base_angle"]
        self.p1_2d = gp_Pnt2d(cos(slot_top_angle) * slot_top_radius, sin(slot_top_angle) * slot_top_radius)
        self.p2_2d = gp_Pnt2d(cos(slot_top_angle) * slot_top_radius, -(sin(slot_top_angle) * slot_top_radius))
        self.p3_2d = gp_Pnt2d(cos(slot_base_angle) * slot_base_radius, sin(slot_base_angle) * slot_base_radius)
        self.p4_2d = gp_Pnt2d(cos(slot_base_angle) * slot_base_radius, -(sin(slot_base_angle) * slot_base_radius))
        self.pt_2d = gp_Pnt2d(slot_top_radius, 0)
        self.pb_2d = gp_Pnt2d(slot_base_radius, 0)
        self.p1_3d = gp_Pnt(self.p1_2d.Coord(1), self.p1_2d.Coord(2), 0)
        self.p2_3d = gp_Pnt(self.p2_2d.Coord(1), self.p2_2d.Coord(2), 0)
        self.p3_3d = gp_Pnt(self.p3_2d.Coord(1), self.p3_2d.Coord(2), 0)
        self.p4_3d = gp_Pnt(self.p4_2d.Coord(1), self.p4_2d.Coord(2), 0)
        self.p1_3d_e = gp_Pnt(self.p1_2d.Coord(1), self.p1_2d.Coord(2), input["active_length"])
        self.p2_3d_e = gp_Pnt(self.p2_2d.Coord(1), self.p2_2d.Coord(2), input["active_length"])
        self.p3_3d_e = gp_Pnt(self.p3_2d.Coord(1), self.p3_2d.Coord(2), input["active_length"])
        self.p4_3d_e = gp_Pnt(self.p4_2d.Coord(1), self.p4_2d.Coord(2), input["active_length"])
        self.sp1 = gp_Pnt2d(cos(slot_opening_top_angle) * hyp_top, sin(slot_opening_top_angle) * hyp_top)
        self.sp2 = gp_Pnt2d(cos(slot_opening_top_angle) * hyp_top, -(sin(slot_opening_top_angle) * hyp_top))
        self.sp3 = gp_Pnt2d(cos(slot_opening_base_angle) * hyp_base, sin(slot_opening_base_angle) * hyp_base)
        self.sp4 = gp_Pnt2d(cos(slot_opening_base_angle) * hyp_base, -(sin(slot_opening_base_angle) * hyp_base))
        self.spt = gp_Pnt2d(hyp_top, 0)
        self.spb = gp_Pnt2d(hyp_base, 0)

    def makeSlot(self):
        arc_top = GCE2d_MakeArcOfCircle(self.p1_2d, self.pt_2d, self.p2_2d).Value()
        edge_top = BRepBuilderAPI_MakeEdge2d(arc_top).Edge()
        edge_left = BRepBuilderAPI_MakeEdge2d(self.p2_2d, self.p4_2d).Edge()
        edge_right = BRepBuilderAPI_MakeEdge2d(self.p1_2d, self.p3_2d).Edge()
        if self.input["slot_type"] == "Curved":
            arc_base = GCE2d_MakeArcOfCircle(self.p3_2d, self.pb_2d, self.p4_2d).Value()
            edge_base = BRepBuilderAPI_MakeEdge2d(arc_base).Edge()
        else:
            edge_base = BRepBuilderAPI_MakeEdge2d(self.p3_2d, self.p4_2d).Edge()
        slot_wire = BRepBuilderAPI_MakeWire(edge_top, edge_left, edge_base, edge_right).Wire()
        slot_face = BRepBuilderAPI_MakeFace(slot_wire, True).Face()
        slot = BRepPrimAPI_MakePrism(slot_face, self.input["active_length_vec"], False, True)
        slot.Build()
        slot = slot.Shape()
        slot_opening = self.makeSlotOpening()
        slot = BRepAlgoAPI_Fuse(slot, slot_opening).Shape()
        return self.makeMultiple(slot)

    def makeSlotOpening(self):
        slot_opening_arc_top = GCE2d_MakeArcOfCircle(self.sp1, self.spt, self.sp2).Value()
        slot_opening_arc_base = GCE2d_MakeArcOfCircle(self.sp3, self.spb, self.sp4).Value()
        slot_opening_edge_top = BRepBuilderAPI_MakeEdge2d(slot_opening_arc_top).Edge()
        slot_opening_edge_base = BRepBuilderAPI_MakeEdge2d(slot_opening_arc_base).Edge()
        slot_opening_edge_left = BRepBuilderAPI_MakeEdge2d(self.sp2, self.sp4).Edge()
        slot_opening_edge_right = BRepBuilderAPI_MakeEdge2d(self.sp1, self.sp3).Edge()
        slot_opening_wire = BRepBuilderAPI_MakeWire(slot_opening_edge_top, slot_opening_edge_left,
                                                    slot_opening_edge_right, slot_opening_edge_base).Wire()
        slot_opening_face = BRepBuilderAPI_MakeFace(slot_opening_wire, True).Face()
        slot_opening = BRepPrimAPI_MakePrism(slot_opening_face, self.input["active_length_vec"], False, True)
        slot_opening.Build()
        return slot_opening.Shape()

    def fillet(self, slot):

        pass

    def makeMultiple(self, slot):
        rot = gp_Trsf()
        num_of_box = 0
        while num_of_box < self.input["num_of_slots"]:
            radians = num_of_box * ((2 * pi) / self.input["num_of_slots"])
            rot.SetRotation(gp_Ax1(), radians)
            slot_rot = BRepBuilderAPI_Transform(slot, rot, False)
            slot_rot.Build()
            slot_rot = slot_rot.Shape()
            if radians == 0:
                fused_slots = BRepAlgoAPI_Fuse(slot, slot_rot).Shape()
            else:
                fused_slots = BRepAlgoAPI_Fuse(fused_slots, slot_rot).Shape()
            num_of_box += 1
        return fused_slots

    def trunc(self):
        pass
