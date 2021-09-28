import math
from error_check import ErrorCheck


class Calculate:

    def __init__(self, input):
        self.input = input
        slot_top_radius = self.input["stator_inner_radius"] + self.input["slot_opening_depth"]
        slot_base_radius = slot_top_radius + self.input["slot_depth"]
        slot_top_circumference = 2 * math.pi * slot_top_radius
        slot_base_circumference = 2 * math.pi * slot_base_radius
        teeth_angle_top = 2 * math.asin(self.input["teeth_width"] / 2 / slot_top_radius)
        if self.input["teeth_width_type"] == "Expanding":
            teeth_angle_base = teeth_angle_top
        elif self.input["teeth_width_type"] == "Manual":
            teeth_angle_top = 2 * math.asin(self.input["inner_teeth_width"] / 2 / slot_top_radius)
            teeth_angle_base = 2 * math.asin(self.input["outer_teeth_width"] / 2 / slot_base_radius)
        else:
            teeth_angle_base = 2 * math.asin(self.input["teeth_width"] / 2 / slot_base_radius)
        teeth_arclength_top = slot_top_circumference * (teeth_angle_top / math.radians(360))
        teeth_arclength_base = slot_base_circumference * (teeth_angle_base / math.radians(360))
        total_teeth_arclength_top = teeth_arclength_top * self.input["num_of_slots"]
        total_teeth_arclength_base = teeth_arclength_base * self.input["num_of_slots"]
        width_slot_top = (slot_top_circumference - total_teeth_arclength_top) / self.input["num_of_slots"]
        width_slot_base = (slot_base_circumference - total_teeth_arclength_base) / self.input["num_of_slots"]
        slot_top_angle = math.radians(360 * (0.5 * width_slot_top / slot_top_circumference))
        slot_base_angle = math.radians(360 * (0.5 * width_slot_base / slot_base_circumference))

        print("slot_top_radius: ", slot_top_radius)
        print("slot_base_radius: ", slot_base_radius)
        print("slot_top_circumference: ", slot_top_circumference)
        print("slot_base_circumference: ", slot_base_circumference)
        print("teeth_angle_top: ", teeth_angle_top)
        print("teeth_angle_base: ", teeth_angle_base)
        print("teeth_arclength_top: ", teeth_arclength_top)
        print("teeth_arclength_base: ", teeth_arclength_base)
        print("total_teeth_arclength_top: ", total_teeth_arclength_top)
        print("total_teeth_arclength_base: ", total_teeth_arclength_base)
        print("width_slot_top: ", width_slot_top)
        print("width_slot_base: ", width_slot_base)
        print("slot_top_angle: ", slot_top_angle)
        print("slot_base_angle: ", slot_base_angle)

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

    def check(self):
        if self.calcResult["width_slot_top"] <= 0:
            return "Inner slot edge has no width!"
        if self.calcResult["width_slot_base"] <= 0:
            return "Outer slot edge has no width! Check manual inputs."


        return None

