from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Trsf, gp_Ax1
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut

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
        # Style of the stator's teeth's feet: [["Default", "Custom" ,"No Feet"]]
        teeth_feet_type = "Custom"
        # Teeth type : [["Constant", "Expanding", "Manual"]]
        teeth_width_type = "Expanding"
        # Fillet type: [["Inner", "Outer", "Both", "No Fillet"]]
        fillet_type = "Both"

        # Original Material
        active_length = 200
        stator_inner_radius = 200
        stator_outer_radius = 400

        # Minimum number of slots = 2
        num_of_slots = 20
        # Constant Teeth Width Parameter: teeth_width
        teeth_width = 20
        # Manual Teeth Width Parameter: inner_teeth_width, outer_teeth_width
        inner_teeth_width = 200
        outer_teeth_width = 20

        slot_depth = 100
        slot_opening_depth = 20
        slot_opening_depth_1 = 10
        # Slot opening must have a [width > 0]
        slot_opening_width = 20

        fillet_radius_base = 20
        fillet_radius_top = 20

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
                      "fillet_type": fillet_type,
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
        body = self.sb.body(points_body)
        points_opening = self.calc.points_opening(points_body)
        if isinstance(points_opening, str):
            return points_opening
        opening = self.sb.opening(points_opening)
        slot = BRepAlgoAPI_Fuse(body, opening).Shape()
        if self.input["fillet_type"] != "No Fillet":
            slot = self.sb.fillet(points_body, slot)
            if isinstance(slot, str):
                return slot
        return self.sb.multiple(slot)

    @staticmethod
    def stator(slots, base):
        return BRepAlgoAPI_Cut(base, slots).Shape()

