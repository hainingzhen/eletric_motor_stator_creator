import math
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_Vec, gp_Trsf, gp_Ax1
from OCC.Core.GCE2d import GCE2d_MakeArcOfCircle
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet2d
from OCC.Display.SimpleGui import init_display
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_WIRE, TopAbs_SHAPE
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform,
                                     BRepBuilderAPI_MakeVertex, BRepBuilderAPI_MakeShape)

display, start_display, add_menu, add_function_to_menu = init_display()

v1 = BRepBuilderAPI_MakeVertex(gp_Pnt(0,0,0)).Vertex()
v2 = BRepBuilderAPI_MakeVertex(gp_Pnt(1,0,0)).Vertex()
v3 = BRepBuilderAPI_MakeVertex(gp_Pnt(1,1,0)).Vertex()
v4 = BRepBuilderAPI_MakeVertex(gp_Pnt(0,1,0)).Vertex()

edge1 = BRepBuilderAPI_MakeEdge(v1, v2).Edge()
edge2 = BRepBuilderAPI_MakeEdge(v2, v3).Edge()
edge3 = BRepBuilderAPI_MakeEdge(v3, v4).Edge()
edge4 = BRepBuilderAPI_MakeEdge(v4, v1).Edge()

wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()

baseFace = BRepBuilderAPI_MakeFace(wire, True).Face()

filletOp = BRepFilletAPI_MakeFillet2d(baseFace)
rFillet1 = 0.1
rFillet2 = 0.03
filletOp.AddFillet(v1, rFillet1)
filletOp.AddFillet(v2, rFillet2)
filletOp.AddFillet(v3, rFillet1)
filletOp.AddFillet(v4, rFillet2)
filletOp.Build()

explorer = TopExp_Explorer(filletOp.Shape(), TopAbs_WIRE)

filletWire = explorer.Current()

newFace = BRepBuilderAPI_MakeFace(filletWire, True).Face()

extrude = BRepPrimAPI_MakePrism(newFace, gp_Vec(0, 0, 5), False, True)
extrude.Build()
extrude = extrude.Shape()

display.DisplayShape(extrude, update=True)

start_display()