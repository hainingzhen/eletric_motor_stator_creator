import math


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
        if input["stator_type"] == "Inner":
            hyp_top = slot_base_radius
            hyp_base = input["stator_outer_radius"]
        else:
            hyp_top = input["stator_inner_radius"]
            hyp_base = hyp_top + input["slot_opening_depth"]
        slot_opening_top_angle = math.asin(input["slot_opening_width"] / 2 / hyp_top)
        slot_opening_base_angle = math.asin(input["slot_opening_width"] / 2 / hyp_base)

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
            "hyp_top": hyp_top,
            "hyp_base": hyp_base,
            "slot_opening_top_angle": slot_opening_top_angle,
            "slot_opening_base_angle": slot_opening_base_angle,
        }

    def check(self):
        if self.calcResult["width_slot_top"] <= 0.5:
            return "Inner slot edge has width below 0.5mm!"
        if self.calcResult["width_slot_base"] <= 0.5:
            return "Outer slot edge has width below 0.5mm! Check manual inputs."
        return None

