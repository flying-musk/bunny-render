import gmsh
import math

stl_in = "Stanford_Bunny.stl"
msh_out = "bunny.msh"

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

gmsh.merge(stl_in)

angle = 40 * math.pi / 180.0
gmsh.model.mesh.classifySurfaces(angle, True, False, math.pi)

gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.01)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.05)

gmsh.model.mesh.generate(2)
gmsh.write(msh_out)
gmsh.finalize()

print(f"saved -> {msh_out}")
