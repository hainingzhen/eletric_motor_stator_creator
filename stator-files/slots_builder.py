from math import cos, sin, pi
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Trsf, gp_Ax1
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge2d, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform, )


class SlotsBuilder:

    def __init__(self, input):
        self.input = input

        # self.p1_2d = gp_Pnt2d(points["inner"][0], points["inner"][1])
        # self.p2_2d = gp_Pnt2d(points["inner"][0], -points["inner"][1])
        # self.p3_2d = gp_Pnt2d(points["outer"][0], points["outer"][1])
        # self.p4_2d = gp_Pnt2d()
        # self.pt_2d = gp_Pnt2d(slot_top_radius, 0)
        # self.pb_2d = gp_Pnt2d(slot_base_radius, 0)
        # self.p1_3d = gp_Pnt(self.p1_2d.Coord(1), self.p1_2d.Coord(2), 0)
        # self.p2_3d = gp_Pnt(self.p2_2d.Coord(1), self.p2_2d.Coord(2), 0)
        # self.p3_3d = gp_Pnt(self.p3_2d.Coord(1), self.p3_2d.Coord(2), 0)
        # self.p4_3d = gp_Pnt(self.p4_2d.Coord(1), self.p4_2d.Coord(2), 0)
        # self.p1_3d_e = gp_Pnt(self.p1_2d.Coord(1), self.p1_2d.Coord(2), input["active_length"])
        # self.p2_3d_e = gp_Pnt(self.p2_2d.Coord(1), self.p2_2d.Coord(2), input["active_length"])
        # self.p3_3d_e = gp_Pnt(self.p3_2d.Coord(1), self.p3_2d.Coord(2), input["active_length"])
        # self.p4_3d_e = gp_Pnt(self.p4_2d.Coord(1), self.p4_2d.Coord(2), input["active_length"])

    def body(self, points):
        inner_point_positive = gp_Pnt2d(points["inner"][0], points["inner"][1])
        inner_point_negative = gp_Pnt2d(points["inner"][0], -points["inner"][1])
        if len(points["inner"]) == 3:
            print("Inner is THREE")
            inner_point_middle = gp_Pnt2d(points["inner"][2], 0)
            inner_arc = GCE2d_MakeArcOfCircle(inner_point_positive, inner_point_middle, inner_point_negative).Value()
            inner_edge = BRepBuilderAPI_MakeEdge2d(inner_arc).Edge()
        else:
            print("Inner is Two")
            inner_edge = BRepBuilderAPI_MakeEdge2d(inner_point_positive, inner_point_negative).Edge()
        outer_point_positive = gp_Pnt2d(points["outer"][0], points["outer"][1])
        outer_point_negative = gp_Pnt2d(points["outer"][0], -points["outer"][1])
        if len(points["outer"]) == 3:
            print("Outer is THRREE")
            outer_point_middle = gp_Pnt2d(points["outer"][2], 0)
            outer_arc = GCE2d_MakeArcOfCircle(outer_point_positive, outer_point_middle, outer_point_negative).Value()
            outer_edge = BRepBuilderAPI_MakeEdge2d(outer_arc).Edge()
        else:
            print("Outer is TWO")
            outer_edge = BRepBuilderAPI_MakeEdge2d(outer_point_positive, outer_point_negative).Edge()
        positive_edge = BRepBuilderAPI_MakeEdge2d(inner_point_positive, outer_point_positive).Edge()
        negative_edge = BRepBuilderAPI_MakeEdge2d(inner_point_negative, outer_point_negative).Edge()
        slot_wire = BRepBuilderAPI_MakeWire(inner_edge, positive_edge, outer_edge, negative_edge).Wire()
        slot_face = BRepBuilderAPI_MakeFace(slot_wire, True).Face()
        slot = BRepPrimAPI_MakePrism(slot_face, self.input["active_length_vec"], False, True)
        slot.Build()
        slot = slot.Shape()
        return slot

    def opening(self, points):
        if len(points) == 2:
            inner_point_positive = gp_Pnt2d(points["inner"][0], points["inner"][1])
            inner_point_negative = gp_Pnt2d(points["inner"][0], -points["inner"][1])
            outer_point_positive = gp_Pnt2d(points["outer"][0], points["outer"][1])
            outer_point_negative = gp_Pnt2d(points["outer"][0], -points["outer"][1])
            outer_edge = BRepBuilderAPI_MakeEdge2d(outer_point_positive, outer_point_negative).Edge()
            positive_edge = BRepBuilderAPI_MakeEdge2d(inner_point_positive, outer_point_positive).Edge()
            negative_edge = BRepBuilderAPI_MakeEdge2d(inner_point_negative, outer_point_negative).Edge()
            if inner_point_positive.Coord(1) == inner_point_negative.Coord(1) \
                    and inner_point_positive.Coord(2) == inner_point_negative.Coord(2):
                opening_wire = BRepBuilderAPI_MakeWire(positive_edge, outer_edge, negative_edge).Wire()
            else:
                inner_edge = BRepBuilderAPI_MakeEdge2d(inner_point_positive, inner_point_negative).Edge()
                opening_wire = BRepBuilderAPI_MakeWire(inner_edge, positive_edge, outer_edge, negative_edge).Wire()
        else:
            pass
        opening_face = BRepBuilderAPI_MakeFace(opening_wire, True).Face()
        opening = BRepPrimAPI_MakePrism(opening_face, self.input["active_length_vec"], False, True)
        opening.Build()
        opening = opening.Shape()
        return opening

    #     # slot_opening_arc_top = GCE2d_MakeArcOfCircle(self.sp1, self.spt, self.sp2).Value()
    #     slot_opening_arc_base = GCE2d_MakeArcOfCircle(self.sp3, self.spb, self.sp4).Value()
    #     # slot_opening_edge_top = BRepBuilderAPI_MakeEdge2d(slot_opening_arc_top).Edge()
    #     slot_opening_edge_top = BRepBuilderAPI_MakeEdge2d(self.sp1, self.sp2).Edge()
    #     slot_opening_edge_base = BRepBuilderAPI_MakeEdge2d(slot_opening_arc_base).Edge()
    #     slot_opening_edge_left = BRepBuilderAPI_MakeEdge2d(self.sp2, self.sp4).Edge()
    #     slot_opening_edge_right = BRepBuilderAPI_MakeEdge2d(self.sp1, self.sp3).Edge()
    #     slot_opening_wire = BRepBuilderAPI_MakeWire(slot_opening_edge_top, slot_opening_edge_left,
    #                                                 slot_opening_edge_right, slot_opening_edge_base).Wire()
    #     slot_opening_face = BRepBuilderAPI_MakeFace(slot_opening_wire, True).Face()
    #     slot_opening = BRepPrimAPI_MakePrism(slot_opening_face, self.input["active_length_vec"], False, True)
    #     slot_opening.Build()
    #     return slot_opening.Shape()

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
