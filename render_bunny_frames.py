import pyvista as pv
import os

pv.OFF_SCREEN = True

mesh0 = pv.read("bunny.vtu")

out_dir = "frames"
os.makedirs(out_dir, exist_ok=True)

pl = pv.Plotter(off_screen=True, window_size=(1024, 768))
pl.set_background("black")
pl.add_text("Stanford Bunny - Gmsh Surface Mesh", font_size=18)

actor = pl.add_mesh(
    mesh0,
    color="lightgray",
    show_edges=True,
    edge_color="white",
    smooth_shading=False,
)

pl.camera_position = "iso"
pl.camera.zoom(1.2)

n_frames = 180
step = 360.0 / n_frames

for i in range(n_frames):
    mesh = mesh0.copy(deep=True)
    mesh.rotate_z(step * i, point=mesh.center, inplace=True)

    # update actor geometry
    pl.remove_actor(actor)
    actor = pl.add_mesh(
        mesh,
        color="lightgray",
        show_edges=True,
        edge_color="white",
        smooth_shading=False,
    )

    fname = f"{out_dir}/frame_{i:04d}.png"
    pl.show(screenshot=fname, auto_close=False)
    if i % 10 == 0:
        print(f"saved {fname}")

pl.close()
print("frames done")
