import meshio

m = meshio.read("bunny.msh")

# Remove metadata that can break PyVista
m.cell_sets = {}
m.point_sets = {}
m.field_data = {}

meshio.write("bunny.vtu", m)

print("saved -> bunny.vtu")
