from math import pi, cos, sin, atan, asin, radians
import sympy as sym


class Calculate:

    def __init__(self, _input):
        self.input = _input
        self.body = self.body()

    def body_calc(self, radius, angle):
        circumference = 2 * pi * radius
        teeth_arclength = circumference * (angle / radians(360))
        total_teeth_arclength = teeth_arclength * self.input["num_of_slots"]
        slot_arclength = (circumference - total_teeth_arclength) / self.input["num_of_slots"]
        return radians(360 * (0.5 * slot_arclength / circumference))

    def body(self):
        if self.input["num_of_slots"] < 2:
            return "Cannot have less than 2 teeth!"
        if self.input["slot_opening_depth"] <= 0:
            return "Slot opening must have a non-zero depth!"
        if self.input["teeth_feet_type"] == "Feet":
            if self.input["slot_opening_depth_1"] > self.input["slot_opening_depth"]:
                return "Feet depth input invalid. Depth 1 cannot be greater than the overall depth."
            if self.input["slot_opening_depth_1"] <= 0:
                return "Feet depth 1 must have a non-zero depth."

        if self.input["stator_type"] == "Outer":
            inner_radius = self.input["stator_inner_radius"] + self.input["slot_opening_depth"]
            outer_radius = inner_radius + self.input["slot_depth"]
        else:
            inner_radius = self.input["stator_outer_radius"] - self.input["slot_depth"]
            outer_radius = self.input["stator_outer_radius"] - self.input["slot_opening_depth"]
        if self.input["teeth_width_type"] == "Expanding":
            teeth_angle_inner = 2 * asin(self.input["teeth_width"] / 2 / inner_radius)
            teeth_angle_outer = teeth_angle_inner
        elif self.input["teeth_width_type"] == "Manual":
            teeth_angle_inner = 2 * asin(self.input["inner_teeth_width"] / 2 / inner_radius)
            teeth_angle_outer = 2 * asin(self.input["outer_teeth_width"] / 2 / outer_radius)
        else:
            teeth_angle_inner = 2 * asin(self.input["teeth_width"] / 2 / inner_radius)
            teeth_angle_outer = 2 * asin(self.input["teeth_width"] / 2 / outer_radius)

        slot_inner_angle = self.body_calc(inner_radius, teeth_angle_inner)
        slot_outer_angle = self.body_calc(outer_radius, teeth_angle_outer)

        inner = [inner_radius * cos(slot_inner_angle), inner_radius * sin(slot_inner_angle)]
        outer = [outer_radius * cos(slot_outer_angle), outer_radius * sin(slot_outer_angle)]
        gradient = (outer[1] - inner[1]) / (outer[0] - inner[0])
        constant = outer[1] - gradient * outer[0]

        if inner[1] <= 0.25:
            return "Inner slot edge has width below 0.25mm!"
        if outer[1] <= 0.25:
            return "Outer slot edge has width below 0.25mm! Check manual inputs."

        return {
            "inner_radius": inner_radius,
            "outer_radius": outer_radius,
            "inner": inner,
            "outer": outer,
            "gradient": gradient,
            "constant": constant
        }

    def points_body(self):
        if self.input["stator_type"] == "Outer":
            if self.input["slot_type"] == "Curved":
                return {
                    "inner": [self.body["inner"][0], self.body["inner"][1], self.body["inner_radius"]],
                    "outer": [self.body["outer"][0], self.body["outer"][1], self.body["outer_radius"]]
                }
            else:
                return {
                    "inner": [self.body["inner"][0], self.body["inner"][1], self.body["inner_radius"]],
                    "outer": [self.body["outer_radius"],
                              self.body["gradient"] * self.body["outer_radius"] + self.body["constant"]]
                }
        else:
            if self.input["slot_type"] == "Curved":
                return {
                    "inner": [self.body["inner"][0], self.body["inner"][1], self.body["inner_radius"]],
                    "outer": [self.body["outer"][0], self.body["outer"][1], self.body["outer_radius"]]
                }
            else:
                return {
                    "inner": [self.body["inner_radius"],
                              self.body["gradient"] * self.body["inner_radius"] + self.body["constant"]],
                    "outer": [self.body["outer"][0], self.body["outer"][1], self.body["outer_radius"]]
                }

    @staticmethod
    def intersect(radius, gradient, constant):
        x, y = sym.symbols('x,y')
        straight_eq = sym.Eq(-gradient * x + y, constant)
        circular_eq = sym.Eq(x**2 + y**2, radius**2)
        results = sym.solve([straight_eq, circular_eq], (x, y))
        for result in results:
            if result[0] > 0:
                x = float(result[0])
                y = float(result[1])
        return x, y

    def points_opening(self, points_body):
        if self.input["stator_type"] == "Outer":
            min_x, min_y = self.intersect(self.input["stator_inner_radius"],
                                          self.body["gradient"],
                                          self.body["constant"])
            if self.input["teeth_feet_type"] == "No Feet":
                return {
                    "inner": [min_x, min_y, self.input["stator_inner_radius"]],
                    "outer": points_body["inner"]
                }
            elif self.input["teeth_feet_type"] == "Default":
                angle_limit = atan(min_y / min_x)

                return {
                    "inner": [],
                    "outer": []
                }
            else:
                inner_y = self.input["slot_opening_width"] / 2
                inner_x = self.input["stator_inner_radius"] * cos(asin(inner_y / self.input["stator_inner_radius"]))
                mid_x, mid_y = self.intersect(self.input["stator_inner_radius"] + self.input["slot_opening_depth_1"],
                                              inner_y / inner_x,
                                              0)
                return {
                    "inner": [inner_x, inner_y, self.input["stator_inner_radius"]],
                    "mid": [mid_x, mid_y],
                    "outer": points_body["inner"]
                }
        else:
            if self.input["teeth_feet_type"] == "No Feet":
                outer_x, outer_y = self.intersect(self.input["stator_outer_radius"],
                                                  self.body["gradient"],
                                                  self.body["constant"])
                return {
                    "inner": points_body["outer"],
                    "outer": [outer_x, outer_y, self.input["stator_outer_radius"]]
                }
            elif self.input["teeth_feet_type"] == "Default":
                x, y = self.intersect(self.input["stator_outer_radius"] - self.input["slot_opening_depth"],
                                      self.body["gradient"],
                                      self.body["constant"])

                pass
            else:
                outer_y = self.input["slot_opening_width"] / 2
                outer_x = self.input["stator_outer_radius"] * cos(asin(outer_y / self.input["stator_outer_radius"]))
                mid_x, mid_y = self.intersect(self.input["stator_outer_radius"] - self.input["slot_opening_depth_1"],
                                              outer_y / outer_x,
                                              0)
                return {
                    "inner": points_body["outer"],
                    "mid": [mid_x, mid_y],
                    "outer": [outer_x, outer_y, self.input["stator_outer_radius"]]
                }
