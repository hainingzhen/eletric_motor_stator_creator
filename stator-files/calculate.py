import math
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Trsf, gp_Ax1
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge2d, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform,
                                     BRepBuilderAPI_MakeVertex)
from error_check import ErrorCheck


class Calculate:

    def __init__(self, input):
        self.input = input
        slot_top_radius = self.input["stator_inner_radius"] + self.input["slot_opening_depth"]
        slot_base_radius = slot_top_radius + self.input["slot_depth"]
        slot_top_circumference = 2 * math.pi * slot_top_radius
        slot_base_circumference = 2 * math.pi * slot_base_radius
        teeth_angle_top = 2 * math.asin(self.input["teeth_width"] / 2 / slot_top_radius)
        teeth_angle_base = 2 * math.asin(self.input["teeth_width"] / 2 / slot_base_radius)
        teeth_arclength_top = slot_top_circumference * (teeth_angle_top / math.radians(360))
        teeth_arclength_base = slot_base_circumference * (teeth_angle_base / math.radians(360))
        total_teeth_arclength_top = teeth_arclength_top * self.input["num_of_slots"]
        total_teeth_arclength_base = teeth_arclength_base * self.input["num_of_slots"]
        width_slot_top = (slot_top_circumference - total_teeth_arclength_top) / self.input["num_of_slots"]
        width_slot_base = (slot_base_circumference - total_teeth_arclength_base) / self.input["num_of_slots"]
        slot_top_angle = math.radians(360 * (0.5 * width_slot_top / slot_top_circumference))
        slot_base_angle = math.radians(360 * (0.5 * width_slot_base / slot_base_circumference))

        self.calcResult = {
            "slot_top_radius": slot_top_radius,
            "slot_base_radius": slot_base_radius,
            "slot_top_circumference": slot_top_circumference,
            "slot_base_circumference": slot_base_circumference,
            "teeth_angle_top": teeth_angle_top,
            "teeth_angle_base": teeth_angle_base,
            "teeth_arclength_top": teeth_arclength_top,
            "teeth_arclength_base": teeth_arclength_base,
            "total_teeth_arclength_top": total_teeth_arclength_top,
            "total_teeth_arclength_base": total_teeth_arclength_base,
            "width_slot_top": width_slot_top,
            "width_slot_base": width_slot_base,
            "slot_top_angle": slot_top_angle,
            "slot_base_angle": slot_base_angle,
        }

    def errorChecking(self):
        err = ErrorCheck(self.calcResult).check()
        return err

    def makeSlots(self):
        p1 = gp_Pnt2d(math.cos(self.calcResult["slot_top_angle"]) * self.calcResult["slot_top_radius"],
                      math.sin(self.calcResult["slot_top_angle"]) * self.calcResult["slot_top_radius"])
        p2 = gp_Pnt2d(math.cos(self.calcResult["slot_top_angle"]) * self.calcResult["slot_top_radius"],
                      -(math.sin(self.calcResult["slot_top_angle"]) * self.calcResult["slot_top_radius"]))
        p3 = gp_Pnt2d(math.cos(self.calcResult["slot_base_angle"]) * self.calcResult["slot_base_radius"],
                      math.sin(self.calcResult["slot_base_angle"]) * self.calcResult["slot_base_radius"])
        p4 = gp_Pnt2d(math.cos(self.calcResult["slot_base_angle"]) * self.calcResult["slot_base_radius"],
                      -(math.sin(self.calcResult["slot_base_angle"]) * self.calcResult["slot_base_radius"]))
        pt = gp_Pnt2d(self.calcResult["slot_top_radius"], 0)
        pb = gp_Pnt2d(self.calcResult["slot_base_radius"], 0)

        arc_top = GCE2d_MakeArcOfCircle(p1, pt, p2).Value()
        arc_base = GCE2d_MakeArcOfCircle(p3, pb, p4).Value()
        edge_top = BRepBuilderAPI_MakeEdge2d(arc_top).Edge()
        edge_left = BRepBuilderAPI_MakeEdge2d(p2, p4).Edge()
        edge_right = BRepBuilderAPI_MakeEdge2d(p1, p3).Edge()
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
