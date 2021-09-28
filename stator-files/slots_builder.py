import math
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Trsf, gp_Ax1
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge2d, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform, )


class SlotsBuilder():

    def __init__(self, calcResult, input):
        self.p1_2d = gp_Pnt2d(math.cos(calcResult["slot_top_angle"]) * calcResult["slot_top_radius"],
                              math.sin(calcResult["slot_top_angle"]) * calcResult["slot_top_radius"])
        self.p2_2d = gp_Pnt2d(math.cos(calcResult["slot_top_angle"]) * calcResult["slot_top_radius"],
                              -(math.sin(calcResult["slot_top_angle"]) * calcResult["slot_top_radius"]))
        self.p3_2d = gp_Pnt2d(math.cos(calcResult["slot_base_angle"]) * calcResult["slot_base_radius"],
                              math.sin(calcResult["slot_base_angle"]) * calcResult["slot_base_radius"])
        self.p4_2d = gp_Pnt2d(math.cos(calcResult["slot_base_angle"]) * calcResult["slot_base_radius"],
                              -(math.sin(calcResult["slot_base_angle"]) * calcResult["slot_base_radius"]))
        self.pt_2d = gp_Pnt2d(calcResult["slot_top_radius"], 0)
        self.pb_2d = gp_Pnt2d(calcResult["slot_base_radius"], 0)

        self.p1_3d = gp_Pnt(self.p1_2d.Coord(1), self.p1_2d.Coord(2), 0)
        self.p2_3d = gp_Pnt(self.p2_2d.Coord(1), self.p2_2d.Coord(2), 0)
        self.p3_3d = gp_Pnt(self.p3_2d.Coord(1), self.p3_2d.Coord(2), 0)
        self.p4_3d = gp_Pnt(self.p4_2d.Coord(1), self.p4_2d.Coord(2), 0)
        self.pt_3d = gp_Pnt(self.pt_2d.Coord(1), 0, 0)
        self.pb_3d = gp_Pnt(self.pb_2d.Coord(1), 0, 0)

    def makeSlots(self):
        arc_top = GCE2d_MakeArcOfCircle(self.p1_2d, self.pt_2d, self.p2_2d).Value()
        arc_base = GCE2d_MakeArcOfCircle(self.p3_2d, self.pb_2d, self.p4_2d).Value()
        edge_top = BRepBuilderAPI_MakeEdge2d(arc_top).Edge()
        edge_left = BRepBuilderAPI_MakeEdge2d(self.p2_2d, self.p4_2d).Edge()
        edge_right = BRepBuilderAPI_MakeEdge2d(self.p1_2d, self.p3_2d).Edge()
        edge_base = BRepBuilderAPI_MakeEdge2d(arc_base).Edge()

        slot_wire = BRepBuilderAPI_MakeWire(edge_top, edge_left, edge_base, edge_right).Wire()
        slot_face = BRepBuilderAPI_MakeFace(slot_wire, True).Face()
        slot = BRepPrimAPI_MakePrism(slot_face, gp_Vec(0, 0, self.input["active_length"]), False, True)
        slot.Build()
        slot = slot.Shape()

        rot = gp_Trsf()
        num_of_box = 0
        while num_of_box < self.input["num_of_slots"]:
            radians = num_of_box * ((2 * math.pi) / self.input["num_of_slots"])
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

    def makeSlotsOpening(self):

        pass
