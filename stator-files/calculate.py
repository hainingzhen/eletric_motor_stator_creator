from math import pi, cos, sin, tan, asin, radians
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
        if self.input["stator_type"] == "Outer":
            inner_radius = self.input["stator_inner_radius"] + self.input["slot_opening_depth"]
            outer_radius = inner_radius + self.input["slot_depth"]
        else:
            inner_radius = self.input["stator_outer_radius"] - self.input["slot_depth"]
            outer_radius = self.input["stator_outer_radius"] - self.input["slot_opening_depth"]
        if self.input["teeth_width_type"] == "Expanding":
            teeth_angle_inner = 2 * asin(self.input["teeth_width"] / 2 / inner_radius)
            teeth_angle_outer = teeth_angle_inner
            teeth_angle_min = teeth_angle_inner
            teeth_angle_max = teeth_angle_inner
        elif self.input["teeth_width_type"] == "Manual":
            teeth_angle_inner = 2 * asin(self.input["inner_teeth_width"] / 2 / inner_radius)
            teeth_angle_outer = 2 * asin(self.input["outer_teeth_width"] / 2 / outer_radius)
            grad = (teeth_angle_outer - teeth_angle_inner) / (outer_radius - inner_radius)
            const = teeth_angle_outer - grad * outer_radius
            teeth_angle_min = grad * self.input["stator_inner_radius"] + const
            teeth_angle_max = grad * self.input["stator_outer_radius"] + const
        else:
            teeth_angle_inner = 2 * asin(self.input["teeth_width"] / 2 / inner_radius)
            teeth_angle_outer = 2 * asin(self.input["teeth_width"] / 2 / outer_radius)
            teeth_angle_min = 2 * asin(self.input["teeth_width"] / 2 / self.input["stator_inner_radius"])
            teeth_angle_max = 2 * asin(self.input["teeth_width"] / 2 / self.input["stator_outer_radius"])

        # print("teeth_angle_inner: ", teeth_angle_inner)
        # print("teeth_angle_outer: ", teeth_angle_outer)
        # print("teeth_angle_max: ", teeth_angle_max)
        # print("teeth_angle_min: ", teeth_angle_min)
        # inner_circumference = 2 * pi * inner_radius
        # outer_circumference = 2 * pi * outer_radius
        # min_circumference = 2 * pi * self.input["stator_inner_radius"]
        # max_circumference = 2 * pi * self.input["stator_outer_radius"]
        # print(max_circumference)
        # teeth_arclength_inner = inner_circumference * (teeth_angle_inner / radians(360))
        # teeth_arclength_outer = outer_circumference * (teeth_angle_outer / radians(360))
        # teeth_arclength_min = min_circumference * (teeth_angle_min / radians(360))
        # teeth_arclength_max = max_circumference * (teeth_angle_max / radians(360))
        # print(teeth_arclength_max)
        # total_teeth_arclength_inner = teeth_arclength_inner * self.input["num_of_slots"]
        # total_teeth_arclength_outer = teeth_arclength_outer * self.input["num_of_slots"]
        # total_teeth_arclength_min = teeth_arclength_min * self.input["num_of_slots"]
        # total_teeth_arclength_max = teeth_arclength_max * self.input["num_of_slots"]
        # print(total_teeth_arclength_max)
        # slot_arclength_inner = (inner_circumference - total_teeth_arclength_inner) / self.input["num_of_slots"]
        # slot_arclength_outer = (outer_circumference - total_teeth_arclength_outer) / self.input["num_of_slots"]
        # slot_arclength_min = (min_circumference - total_teeth_arclength_min) / self.input["num_of_slots"]
        # slot_arclength_max = (max_circumference - total_teeth_arclength_max) / self.input["num_of_slots"]
        # print(slot_arclength_max)
        # slot_inner_angle = radians(360 * (0.5 * slot_arclength_inner / inner_circumference))
        # slot_outer_angle = radians(360 * (0.5 * slot_arclength_outer / outer_circumference))
        # slot_min_angle = radians(360 * (0.5 * slot_arclength_min / min_circumference))
        # slot_max_angle = radians(360 * (0.5 * slot_arclength_max / max_circumference))

        slot_inner_angle = self.body_calc(inner_radius, teeth_angle_inner)
        slot_outer_angle = self.body_calc(outer_radius, teeth_angle_outer)
        slot_min_angle = self.body_calc(self.input["stator_inner_radius"], teeth_angle_min)
        slot_max_angle = self.body_calc(self.input["stator_outer_radius"], teeth_angle_max)

        min_y = self.input["stator_inner_radius"] * sin(slot_min_angle)
        max_y = self.input["stator_outer_radius"] * sin(slot_max_angle)
        inner = [inner_radius * cos(slot_inner_angle), inner_radius * sin(slot_inner_angle)]
        outer = [outer_radius * cos(slot_outer_angle), outer_radius * sin(slot_outer_angle)]
        gradient = (outer[1] - inner[1]) / (outer[0] - inner[0])
        constant = outer[1] - gradient * outer[0]

        # print("min_y: ", min_y)
        # print("max_y: ", max_y)
        # print("inner[1]: ", inner[1])
        # print("outer[1]: ", outer[1])

        if inner[1] <= 0.25:
            return "Inner slot edge has width below 0.5mm!"
        if outer[1] <= 0.25:
            return "Outer slot edge has width below 0.5mm! Check manual inputs."
        # if self.input["stator_type"] == "Outer":
        #     if self.input["slot_opening_width"]/2 >= min_y or self.input["slot_opening_width"]/2 >= inner[1]:
        #         return "Slot feet opening width is too large."
        # else:
        #     if self.input["slot_opening_width"]/2 >= outer[1] or self.input["slot_opening_width"]/2 >= max_y:
        #         # return "Slot feet opening width is too large."
        #         print("PROBLEM")
        #         pass

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

    def intersect(self, radius):
        x, y = sym.symbols('x,y')
        straight_eq = sym.Eq(-self.body["gradient"]*x + y, self.body["constant"])
        circular_eq = sym.Eq(x**2 + y**2, radius**2)
        results = sym.solve([straight_eq, circular_eq], (x, y))
        for result in results:
            if result[0] > 0:
                x = float(result[0])
                y = float(result[1])
        return x, y

    def points_opening(self, points_body):
        if self.input["stator_type"] == "Outer":
            if self.input["teeth_feet_type"] == "No Feet":
                inner_x, inner_y = self.intersect(self.input["stator_inner_radius"])
                return {
                    "inner": [inner_x, inner_y, self.input["stator_inner_radius"]],
                    "outer": points_body["inner"]
                }
            else:
                return {
                    "inner": [],
                    "mid": [],
                    "outer": []
                }
        else:
            if self.input["teeth_feet_type"] == "No Feet":
                outer_x, outer_y = self.intersect(self.input["stator_outer_radius"])
                return {
                    "inner": points_body["outer"],
                    "outer": [outer_x, outer_y, self.input["stator_outer_radius"]]
                }
            else:
                return {
                    "inner": [],
                    "mid": [],
                    "outer": []
                }


# return {
#     "inner_radius": inner_radius,
#     "outer_radius": outer_radius,
#     "mid_radius": mid_radius,
#     "inner_circumference": inner_circumference,
#     "outer_circumference": outer_circumference,
#     "mid_circumference": mid_circumference,
#     "teeth_angle_inner": teeth_angle_inner,
#     "teeth_angle_outer": teeth_angle_outer,
#     "teeth_angle_mid": teeth_angle_mid,
#     "teeth_arclength_inner": teeth_arclength_inner,
#     "teeth_arclength_outer": teeth_arclength_outer,
#     "teeth_arclength_mid": teeth_arclength_mid,
#     "total_teeth_arclength_inner": total_teeth_arclength_inner,
#     "total_teeth_arclength_outer": total_teeth_arclength_outer,
#     "total_teeth_arclength_mid": total_teeth_arclength_mid,
#     "slot_arclength_inner": slot_arclength_inner,
#     "slot_arclength_outer": slot_arclength_outer,
#     "slot_arclength_mid": slot_arclength_mid,
#     "slot_inner_angle": slot_inner_angle,
#     "slot_outer_angle": slot_outer_angle,
#     "slot_mid_angle": slot_mid_angle,
# }