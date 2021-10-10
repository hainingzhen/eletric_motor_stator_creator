from math import pi, cos, sin, asin, radians
from OCC.Core.gp import gp_Pnt, gp_Vec


class Calculate:

    def __init__(self, input):
        self.input = input
        self.calcResult = self.calculate()

    def calculate(self):
        if self.input["stator_type"] == "Outer":
            inner_radius = self.input["stator_inner_radius"]
            outer_radius = inner_radius + self.input["slot_depth"]
            mid_radius = inner_radius + self.input["slot_opening_depth"]
        else:
            inner_radius = self.input["stator_outer_radius"] - self.input["slot_depth"]
            outer_radius = self.input["stator_outer_radius"]
            mid_radius = outer_radius - self.input["slot_opening_depth"]
        inner_circumference = 2 * pi * inner_radius
        outer_circumference = 2 * pi * outer_radius
        mid_circumference = 2 * pi * mid_radius
        if self.input["teeth_width_type"] == "Expanding":
            teeth_angle_inner = 2 * asin(self.input["teeth_width"] / 2 / inner_radius)
            teeth_angle_mid = teeth_angle_inner
            teeth_angle_outer = teeth_angle_inner
        elif self.input["teeth_width_type"] == "Manual":
            teeth_angle_inner = 2 * asin(self.input["inner_teeth_width"] / 2 / inner_radius)
            teeth_angle_outer = 2 * asin(self.input["outer_teeth_width"] / 2 / outer_radius)
            percentage = (mid_radius - inner_radius) / (outer_radius - inner_radius)
            teeth_angle_mid = teeth_angle_inner + percentage * (teeth_angle_outer - teeth_angle_inner)
        else:
            teeth_angle_inner = 2 * asin(self.input["teeth_width"] / 2 / inner_radius)
            teeth_angle_outer = 2 * asin(self.input["teeth_width"] / 2 / outer_radius)
            teeth_angle_mid = 2 * asin(self.input["teeth_width"] / 2 / mid_radius)
        teeth_arclength_inner = inner_circumference * (teeth_angle_inner / radians(360))
        teeth_arclength_outer = outer_circumference * (teeth_angle_outer / radians(360))
        teeth_arclength_mid = mid_circumference * (teeth_angle_mid / radians(360))
        total_teeth_arclength_inner = teeth_arclength_inner * self.input["num_of_slots"]
        total_teeth_arclength_outer = teeth_arclength_outer * self.input["num_of_slots"]
        total_teeth_arclength_mid = teeth_arclength_mid * self.input["num_of_slots"]
        slot_arclength_inner = (inner_circumference - total_teeth_arclength_inner) / self.input["num_of_slots"]
        slot_arclength_outer = (outer_circumference - total_teeth_arclength_outer) / self.input["num_of_slots"]
        slot_arclength_mid = (mid_circumference - total_teeth_arclength_mid) / self.input["num_of_slots"]
        slot_inner_angle = radians(360 * (0.5 * slot_arclength_inner / inner_circumference))
        slot_outer_angle = radians(360 * (0.5 * slot_arclength_outer / outer_circumference))
        slot_mid_angle = radians(360 * (0.5 * slot_arclength_mid / mid_circumference))

        return {
            "inner_radius": inner_radius,
            "outer_radius": outer_radius,
            "mid_radius": mid_radius,
            "inner_circumference": inner_circumference,
            "outer_circumference": outer_circumference,
            "mid_circumference": mid_circumference,
            "teeth_angle_inner": teeth_angle_inner,
            "teeth_angle_outer": teeth_angle_outer,
            "teeth_angle_mid": teeth_angle_mid,
            "teeth_arclength_inner": teeth_arclength_inner,
            "teeth_arclength_outer": teeth_arclength_outer,
            "teeth_arclength_mid": teeth_arclength_mid,
            "total_teeth_arclength_inner": total_teeth_arclength_inner,
            "total_teeth_arclength_outer": total_teeth_arclength_outer,
            "total_teeth_arclength_mid": total_teeth_arclength_mid,
            "slot_arclength_inner": slot_arclength_inner,
            "slot_arclength_outer": slot_arclength_outer,
            "slot_arclength_mid": slot_arclength_mid,
            "slot_inner_angle": slot_inner_angle,
            "slot_outer_angle": slot_outer_angle,
            "slot_mid_angle": slot_mid_angle,
        }

    def check(self):
        if self.calcResult["slot_arclength_inner"] <= 0.5:
            return "Inner slot edge has width below 0.5mm!"
        if self.calcResult["slot_arclength_outer"] <= 0.5:
            return "Outer slot edge has width below 0.5mm! Check manual inputs."
        return None

    def points(self):
        inner_radius = self.calcResult["inner_radius"]
        mid_radius = self.calcResult["mid_radius"]
        outer_radius = self.calcResult["outer_radius"]
        inner = [inner_radius * cos(self.calcResult["slot_inner_angle"]),
                 inner_radius * sin(self.calcResult["slot_inner_angle"])]
        mid = [mid_radius * cos(self.calcResult["slot_mid_angle"]),
               mid_radius * sin(self.calcResult["slot_mid_angle"])]
        outer = [outer_radius * cos(self.calcResult["slot_outer_angle"]),
                 outer_radius * sin(self.calcResult["slot_outer_angle"])]
        gradient = (outer[1] - inner[1]) / (outer[0] - inner[0])
        constant = outer[1] - gradient * outer[0]
        if self.input["stator_type"] == "Outer":
            if self.input["slot_type"] == "Curved":
                slot_coord = {
                    "inner": {"1": [mid[0], mid[1]]},
                    "outer": {"1": [outer[0], outer[1]], "2": [outer_radius, 0]}
                }
            else:
                slot_coord = {
                    "inner": {"1": [mid[0], mid[1]]},
                    "outer": {"1": [outer_radius, gradient * outer_radius + constant]}
                }
        else:
            if self.input["slot_type"] == "Curved":
                slot_coord = {
                    "inner": {"1": [inner[0], inner[1]], "2": [inner_radius, 0]},
                    "outer": {"1": [mid[0], mid[1]]}
                }
            else:
                slot_coord = {
                    "inner": {"1": [inner_radius, gradient * inner_radius + constant]},
                    "outer": {"1": [mid[0], mid[1]]}
                }

        print(slot_coord)

        return slot_coord
