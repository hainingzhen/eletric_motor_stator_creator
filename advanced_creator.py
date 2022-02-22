from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut

from calculate import Calculate
from slots_builder import SlotsBuilder


class AdvancedStatorCreator:

    def __init__(self, _input):
        self.input = _input
        if self.input["teeth_feet_type"] == "Custom" and self.input["fillet_type"] != "No Fillet":
            if self.input["stator_type"] == "Inner":
                self.input["fillet_type"] = "Inner"
            else:
                self.input["fillet_type"] = "Outer"
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
        if isinstance(points_body, str):
            return points_body
        body = self.sb.body(points_body)
        points_opening = self.calc.points_opening(points_body)
        if isinstance(points_opening, str):
            return points_opening
        opening = self.sb.opening(points_opening)
        slot = BRepAlgoAPI_Fuse(body, opening).Shape()
        if self.input["fillet_type"] != "No Fillet":
            print("here")
            slot = self.sb.fillet(points_body, slot)
            if isinstance(slot, str):
                return slot
        return self.sb.multiple(slot)

    @staticmethod
    def stator(slots, base):
        return BRepAlgoAPI_Cut(base, slots).Shape()

