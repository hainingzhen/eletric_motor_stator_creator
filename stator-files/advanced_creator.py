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
        stator_type = "Outer"
        # Slot Bottom Type : [["Curved", "Flat"]]
        slot_type = "Curved"
        # Slot Fillet Type: [["Fillet" , "No Fillet"]]
        slot_fillet_type = "No Fillet"
        # Style of the stator's teeth's feet: [["Flat", "Tilt" ,"No Feet"]]
        teeth_feet_type = "Flat"
        # Teeth type : [["Constant", "Expanding", "Manual"]]
        teeth_width_type = "Manual"

        # Original Material
        active_length = 90
        stator_inner_radius = 80
        stator_outer_radius = 200

        num_of_slots = 14
        teeth_width = 15  # Using teeth_width instead of slot top and base widths.
        inner_teeth_width = 15
        outer_teeth_width = 30
        slot_opening_depth = 5
        slot_opening_width = 10  # Constant slot opening width
        slot_depth = 70
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
                      "slot_opening_width": slot_opening_width,
                      "slot_depth": slot_depth,
                      "fillet_radius_base": fillet_radius_base,
                      "fillet_radius_top": fillet_radius_top,
                      }

    def makeBase(self):
        inner_cut = BRepPrimAPI_MakeCylinder(self.input["stator_inner_radius"], self.input["active_length"]).Shape()
        base = BRepPrimAPI_MakeCylinder(self.input["stator_outer_radius"], self.input["active_length"]).Shape()
        return BRepAlgoAPI_Cut(base, inner_cut).Shape()

    def makeSlots(self):
        calc = Calculate(self.input)
        err = calc.check()
        if err is not None:
            print("Error Msg: ", err)
            return err
        sb = SlotsBuilder(calc.calcResult, self.input)
        return sb.makeSlot()

    def makeStator(self, slots, base):
        return BRepAlgoAPI_Cut(base, slots).Shape()


# This should be called by the PyQt5 code
def main():
    asc = AdvancedStatorCreator()
    base = asc.makeBase()
    slots = asc.makeSlots()
    if isinstance(slots, str):
        return slots
    stator = asc.makeStator(slots, base)

    # Display the stator if its made
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(stator, update=True)
    start_display()


if __name__ == '__main__':
    main()

