from math import cos, sin, pi, trunc
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Trsf, gp_Ax1, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.BRep import BRep_Tool
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Edge
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge2d, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform, )


class SlotsBuilder:

    def __init__(self, _input):
        self.input = _input

    def body(self, points):
        inner_point_positive = gp_Pnt2d(points["inner"][0], points["inner"][1])
        inner_point_negative = gp_Pnt2d(points["inner"][0], -points["inner"][1])
        if len(points["inner"]) == 3:
            inner_point_middle = gp_Pnt2d(points["inner"][2], 0)
            inner_arc = GCE2d_MakeArcOfCircle(inner_point_positive, inner_point_middle, inner_point_negative).Value()
            inner_edge = BRepBuilderAPI_MakeEdge2d(inner_arc).Edge()
        else:
            inner_edge = BRepBuilderAPI_MakeEdge2d(inner_point_positive, inner_point_negative).Edge()
        outer_point_positive = gp_Pnt2d(points["outer"][0], points["outer"][1])
        outer_point_negative = gp_Pnt2d(points["outer"][0], -points["outer"][1])
        if len(points["outer"]) == 3:
            outer_point_middle = gp_Pnt2d(points["outer"][2], 0)
            outer_arc = GCE2d_MakeArcOfCircle(outer_point_positive, outer_point_middle, outer_point_negative).Value()
            outer_edge = BRepBuilderAPI_MakeEdge2d(outer_arc).Edge()
        else:
            outer_edge = BRepBuilderAPI_MakeEdge2d(outer_point_positive, outer_point_negative).Edge()
        positive_edge = BRepBuilderAPI_MakeEdge2d(inner_point_positive, outer_point_positive).Edge()
        negative_edge = BRepBuilderAPI_MakeEdge2d(inner_point_negative, outer_point_negative).Edge()
        slot_wire = BRepBuilderAPI_MakeWire(inner_edge, positive_edge, outer_edge, negative_edge).Wire()
        slot_face = BRepBuilderAPI_MakeFace(slot_wire, True).Face()
        slot = BRepPrimAPI_MakePrism(slot_face, gp_Vec(0, 0, self.input["active_length"]), False, True)
        slot.Build()
        return slot.Shape()

    def opening(self, points):
        if len(points) == 2:
            if len(points["inner"]) == 3:
                inner_point_p = gp_Pnt2d(points["inner"][0], points["inner"][1])
                inner_point_n = gp_Pnt2d(points["inner"][0], -points["inner"][1])
                inner_point_m = gp_Pnt2d(points["inner"][2], 0)
                inner_arc = GCE2d_MakeArcOfCircle(inner_point_p, inner_point_m, inner_point_n).Value()
                inner_edge = BRepBuilderAPI_MakeEdge2d(inner_arc).Edge()
            else:
                inner_point_p = gp_Pnt2d(points["inner"][0], points["inner"][1])
                inner_point_n = gp_Pnt2d(points["inner"][0], -points["inner"][1])
                inner_edge = BRepBuilderAPI_MakeEdge2d(inner_point_p, inner_point_n).Edge()
            if len(points["outer"]) == 3:
                outer_point_p = gp_Pnt2d(points["outer"][0], points["outer"][1])
                outer_point_n = gp_Pnt2d(points["outer"][0], -points["outer"][1])
                outer_point_m = gp_Pnt2d(points["outer"][2], 0)
                outer_arc = GCE2d_MakeArcOfCircle(outer_point_p, outer_point_m, outer_point_n).Value()
                outer_edge = BRepBuilderAPI_MakeEdge2d(outer_arc).Edge()
            else:
                outer_point_p = gp_Pnt2d(points["outer"][0], points["outer"][1])
                outer_point_n = gp_Pnt2d(points["outer"][0], -points["outer"][1])
                outer_edge = BRepBuilderAPI_MakeEdge2d(outer_point_p, outer_point_n).Edge()
            positive_edge = BRepBuilderAPI_MakeEdge2d(inner_point_p, outer_point_p).Edge()
            negative_edge = BRepBuilderAPI_MakeEdge2d(inner_point_n, outer_point_n).Edge()
            opening_wire = BRepBuilderAPI_MakeWire(inner_edge, positive_edge, outer_edge, negative_edge).Wire()
        else:
            if len(points["inner"]) == 3:
                inner_point_p = gp_Pnt2d(points["inner"][0], points["inner"][1])
                inner_point_n = gp_Pnt2d(points["inner"][0], -points["inner"][1])
                inner_point_m = gp_Pnt2d(points["inner"][2], 0)
                inner_arc = GCE2d_MakeArcOfCircle(inner_point_p, inner_point_m, inner_point_n).Value()
                inner_edge = BRepBuilderAPI_MakeEdge2d(inner_arc).Edge()
            else:
                inner_point_p = gp_Pnt2d(points["inner"][0], points["inner"][1])
                inner_point_n = gp_Pnt2d(points["inner"][0], -points["inner"][1])
                inner_edge = BRepBuilderAPI_MakeEdge2d(inner_point_p, inner_point_n).Edge()
            if len(points["outer"]) == 3:
                outer_point_p = gp_Pnt2d(points["outer"][0], points["outer"][1])
                outer_point_n = gp_Pnt2d(points["outer"][0], -points["outer"][1])
                outer_point_m = gp_Pnt2d(points["outer"][2], 0)
                outer_arc = GCE2d_MakeArcOfCircle(outer_point_p, outer_point_m, outer_point_n).Value()
                outer_edge = BRepBuilderAPI_MakeEdge2d(outer_arc).Edge()
            else:
                outer_point_p = gp_Pnt2d(points["outer"][0], points["outer"][1])
                outer_point_n = gp_Pnt2d(points["outer"][0], -points["outer"][1])
                outer_edge = BRepBuilderAPI_MakeEdge2d(outer_point_p, outer_point_n).Edge()
            mid_point_p = gp_Pnt2d(points["mid"][0], points["mid"][1])
            mid_point_n = gp_Pnt2d(points["mid"][0], -points["mid"][1])
            positive_edge_inner = BRepBuilderAPI_MakeEdge2d(inner_point_p, mid_point_p).Edge()
            positive_edge_outer = BRepBuilderAPI_MakeEdge2d(mid_point_p, outer_point_p).Edge()
            negative_edge_inner = BRepBuilderAPI_MakeEdge2d(inner_point_n, mid_point_n).Edge()
            negative_edge_outer = BRepBuilderAPI_MakeEdge2d(mid_point_n, outer_point_n).Edge()
            opening_wire = BRepBuilderAPI_MakeWire(inner_edge, positive_edge_inner,
                                                   positive_edge_outer, outer_edge).Wire()
            opening_wire = BRepBuilderAPI_MakeWire(opening_wire, negative_edge_outer).Wire()
            opening_wire = BRepBuilderAPI_MakeWire(opening_wire, negative_edge_inner).Wire()
        opening_face = BRepBuilderAPI_MakeFace(opening_wire, True).Face()
        opening = BRepPrimAPI_MakePrism(opening_face, gp_Vec(0, 0, self.input["active_length"]), False, True)
        opening.Build()
        return opening.Shape()

    def fillet(self, points, slot):
        inner_coord_positive = self._trunc([points["inner"][0], points["inner"][1], 0])
        inner_coord_negative = self._trunc([points["inner"][0], -points["inner"][1], 0])
        outer_coord_positive = self._trunc([points["outer"][0], points["outer"][1], 0])
        outer_coord_negative = self._trunc([points["outer"][0], -points["outer"][1], 0])
        inner_coord_positive_e = self._trunc([points["inner"][0], points["inner"][1], self.input["active_length"]])
        inner_coord_negative_e = self._trunc([points["inner"][0], -points["inner"][1], self.input["active_length"]])
        outer_coord_positive_e = self._trunc([points["outer"][0], points["outer"][1], self.input["active_length"]])
        outer_coord_negative_e = self._trunc([points["outer"][0], -points["outer"][1], self.input["active_length"]])

        fillets = BRepFilletAPI_MakeFillet(slot)
        edges = TopExp_Explorer(slot, TopAbs_EDGE)
        while edges.More():
            current_edge = edges.Current()
            first_point = BRep_Tool().Pnt(ShapeAnalysis_Edge().FirstVertex(current_edge))
            last_point = BRep_Tool().Pnt(ShapeAnalysis_Edge().LastVertex(current_edge))
            first_point = self._trunc([first_point.Coord(1), first_point.Coord(2), first_point.Coord(3)])
            last_point = self._trunc([last_point.Coord(1), last_point.Coord(2), last_point.Coord(3)])
            if first_point == inner_coord_positive and last_point == inner_coord_positive_e:
                if self.input["fillet_type"] == "Both" or self.input["fillet_type"] == "Inner":
                    fillets.Add(self.input["fillet_radius_inner"], current_edge)
            elif first_point == inner_coord_negative and last_point == inner_coord_negative_e:
                if self.input["fillet_type"] == "Both" or self.input["fillet_type"] == "Inner":
                    fillets.Add(self.input["fillet_radius_inner"], current_edge)
            elif first_point == outer_coord_positive and last_point == outer_coord_positive_e:
                if self.input["fillet_type"] == "Both" or self.input["fillet_type"] == "Outer":
                    fillets.Add(self.input["fillet_radius_outer"], current_edge)
            elif first_point == outer_coord_negative and last_point == outer_coord_negative_e:
                if self.input["fillet_type"] == "Both" or self.input["fillet_type"] == "Outer":
                    fillets.Add(self.input["fillet_radius_outer"], current_edge)
            edges.Next()
        fillets.Build()
        try:
            slot = fillets.Shape()
        except RuntimeError:
            return "Fillet radius is too large for the stator slot."
        return slot

    def multiple(self, slot):
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

    @staticmethod
    def _trunc(arr):
        ret = []
        for coord in arr:
            ret.append(trunc(coord * 1_000_000) / 1_000_000)
        return ret
