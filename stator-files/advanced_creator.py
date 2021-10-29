import math
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Trsf, gp_Ax1
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Display.SimpleGui import init_display
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Edge
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge2d, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform,
                                     BRepBuilderAPI_MakeVertex)

from calculate import Calculate
from slots_builder import SlotsBuilder


class AdvancedStatorCreator:

    def __init__(self):
        # Stator Type : [["Inner", "Outer"]]
        stator_type = "Inner"
        # Slot Bottom Type : [["Curved", "Flat"]]
        slot_type = "Curved"
        # Slot Fillet Type: [["Fillet" , "No Fillet"]]
        slot_fillet_type = "No Fillet"
        # Style of the stator's teeth's feet: [["Feet" ,"No Feet"]]
        teeth_feet_type = "Feet"
        # Teeth type : [["Constant", "Expanding", "Manual"]]
        teeth_width_type = "Expanding"

        # Original Material
        active_length = 90
        stator_inner_radius = 200
        stator_outer_radius = 400

        # Minimum number of slots = 2
        num_of_slots = 15
        # Constant Teeth Width Parameter: teeth_width
        teeth_width = 20
        # Manual Teeth Width Parameter: inner_teeth_width, outer_teeth_width
        inner_teeth_width = 200
        outer_teeth_width = 20

        slot_opening_depth = 10
        slot_opening_depth_1 = 5
        slot_opening_width = 12 # Must have a width
        slot_depth = 100

        fillet_radius_base = 5
        fillet_radius_top = 2

        self.input = {"stator_type": stator_type,
                      "slot_type": slot_type,
                      "slot_fillet_type": slot_fillet_type,
                      "teeth_feet_type": teeth_feet_type,
                      "teeth_width_type": teeth_width_type,
                      "active_length": active_length,
                      "active_length_vec": gp_Vec(0, 0, active_length),
                      "stator_inner_radius": stator_inner_radius,
                      "stator_outer_radius": stator_outer_radius,
                      "num_of_slots": num_of_slots,
                      "teeth_width": teeth_width,
                      "inner_teeth_width": inner_teeth_width,
                      "outer_teeth_width": outer_teeth_width,
                      "slot_opening_depth": slot_opening_depth,
                      "slot_opening_depth_1": slot_opening_depth_1,
                      "slot_opening_width": slot_opening_width,
                      "slot_depth": slot_depth,
                      "fillet_radius_base": fillet_radius_base,
                      "fillet_radius_top": fillet_radius_top,
                      }

        self.calc = Calculate(self.input)
        self.sb = SlotsBuilder(self.input)

    def base(self):
        inner_cut = BRepPrimAPI_MakeCylinder(self.input["stator_inner_radius"], self.input["active_length"]).Shape()
        base = BRepPrimAPI_MakeCylinder(self.input["stator_outer_radius"], self.input["active_length"]).Shape()
        return BRepAlgoAPI_Cut(base, inner_cut).Shape()

    def slot(self):
        calc_body = self.calc.body
        if isinstance(calc_body, str):
            return calc_body
        points_body = self.calc.points_body()
        print("points_body: ", points_body)
        body = self.sb.body(points_body)
        # calc_opening = self.calc.opening
        # if isinstance(calc_opening, str):
        #     return calc_opening
        points_opening = self.calc.points_opening(points_body)
        print("points_opening: ", points_opening)
        opening = self.sb.opening(points_opening)
        slot = BRepAlgoAPI_Fuse(body, opening).Shape()
        # slots = self.sb.makeMultiple(slot)
        # slots = self.sb.makeMultiple(body)
        slots = self.sb.multiple(slot)
        return slots

    def stator(self, slots, base):
        return BRepAlgoAPI_Cut(base, slots).Shape()

