import os
import subprocess
import numpy as np
import pyvista as pv

pv.OFF_SCREEN = True
os.environ["PYVISTA_OFF_SCREEN"] = "true"

STL_IN = "Stanford_Bunny.stl"
OUT_VIDEO = "bunny_mesh.mov"

n_frames = 49
# n_frames = 180
fps = 30
step_deg = 360.0 / n_frames
w, h = 1024, 768

mesh = pv.read(STL_IN)

pl = pv.Plotter(off_screen=True, window_size=(w, h))
pl.set_background("black")
actor = pl.add_mesh(
    mesh,
    color="lightgray",
    show_edges=True,
    edge_color="white",
)
pl.camera_position = "iso"
pl.camera.zoom(1.2)

pl.show(auto_close=False)

ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-f",
    "rawvideo",
    "-pix_fmt",
    "rgb24",  # RGB (3 channels)
    "-s:v",
    f"{w}x{h}",
    "-r",
    str(fps),
    "-i",
    "-",  # stdin
    "-an",
    "-c:v",
    "prores_ks",
    "-profile:v",
    "3",  # ProRes 422 HQ
    "-pix_fmt",
    "yuv422p10le",  # ProRes output format
    OUT_VIDEO,
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

cam = pl.camera
print("Starting rendering frames...")

for i in range(n_frames):
    cam.Azimuth(step_deg)
    pl.render()
    img = pl.image

    if img.shape[2] == 4:
        img = img[:, :, :3]

    img = np.ascontiguousarray(img).astype(np.uint8)
    proc.stdin.write(img.tobytes())

    if i % 30 == 0:
        print(f"Rendered {i}/{n_frames} frames")

proc.stdin.close()
proc.wait()
pl.close()

print(f"Done! Video saved -> {OUT_VIDEO}")


# module load ffmpeg
# python render_stl_movie.py

# module load ffmpeg && python render_stl_movie.py
