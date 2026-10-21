"""Render a multi-frame XYZ trajectory to MP4 with the pip version of OVITO.

XYZ format assumed:
    line 1      : number of atoms
    line 2      : frame N        (N = MD step number)
    line 3..    : element x y z
    (repeated for every frame)
"""
import math

from ovito.io import import_file
from ovito.modifiers import (
    CreateBondsModifier,
    SelectTypeModifier,
    ComputePropertyModifier,
    ClearSelectionModifier,
    CalculateDisplacementsModifier,
    ColorCodingModifier,
)
from ovito.vis import Viewport, TextLabelOverlay, OpenGLRenderer

# ---------------- User settings ----------------
XYZ_FILE = "traj.xyz"
OUT_MP4 = "traj.mp4"

DT_FS = 0.5                # MD timestep [fs]; time = N * DT_FS

TARGET_TYPE = "O"          # element whose radius is changed
TARGET_RADIUS = 0.8        # new radius for TARGET_TYPE [Angstrom]

BOND_CUTOFF = 1.6          # bond cutoff distance [Angstrom]
DISP_MAX = 5.0             # upper limit of color scale [Angstrom]

CAMERA_POS = (30.0, -40.0, 25.0)   # camera position
CAMERA_DIR = (-0.5, 1.0, -0.4)     # viewing direction
FOV_DEG = 35.0                     # field of view [deg]

IMAGE_SIZE = (1280, 720)
FPS = 20
# -----------------------------------------------

# Read the step number N from line 2 of every frame (used for the time label)
with open(XYZ_FILE) as f:
    lines = f.read().splitlines()
natoms = int(lines[0].split()[0])
steps = [int(lines[i + 1].split()[-1]) for i in range(0, len(lines), natoms + 2)
         if lines[i].strip()]

# Plain XYZ needs an explicit column mapping
pipeline = import_file(XYZ_FILE, columns=["Particle Type",
                                          "Position.X", "Position.Y", "Position.Z"])
pipeline.add_to_scene()

# Particle size 50 %
pipeline.source.data.particles.vis.scaling = 0.5

# Create bonds
bonds_mod = CreateBondsModifier(cutoff=BOND_CUTOFF)
bonds_mod.vis.width = 0.2
pipeline.modifiers.append(bonds_mod)

# Change radius of one element only: Select type -> Compute property (selected only) -> Clear selection
pipeline.modifiers.append(SelectTypeModifier(property="Particle Type", types={TARGET_TYPE}))
pipeline.modifiers.append(ComputePropertyModifier(output_property="Radius",
                                                  expressions=[str(TARGET_RADIUS)],
                                                  only_selected=True))
pipeline.modifiers.append(ClearSelectionModifier())

# Displacement from frame 0 -> magnitude via Compute property -> Color coding
pipeline.modifiers.append(CalculateDisplacementsModifier(reference_frame=0))
pipeline.modifiers.append(ComputePropertyModifier(
    output_property="Disp",
    expressions=["sqrt(Displacement.X^2 + Displacement.Y^2 + Displacement.Z^2)"]))
pipeline.modifiers.append(ColorCodingModifier(property="Disp",
                                              start_value=0.0, end_value=DISP_MAX,
                                              gradient=ColorCodingModifier.Viridis()))

# Store simulation time [fs] as a global attribute for the text label
def add_time(frame, data):
    data.attributes["Time"] = steps[frame] * DT_FS
pipeline.modifiers.append(add_time)

# Manual camera
vp = Viewport(type=Viewport.Type.Perspective,
              camera_pos=CAMERA_POS,
              camera_dir=CAMERA_DIR,
              fov=math.radians(FOV_DEG))

# Time label in the upper-left corner (upper-left is the default alignment, so no Qt import is needed)
vp.overlays.append(TextLabelOverlay(
    text="t = [Time] fs",
    offset_x=0.02, offset_y=-0.02,
    font_size=0.05,
    text_color=(0.0, 0.0, 0.0)))

# Render all frames to MP4
vp.render_anim(filename=OUT_MP4, size=IMAGE_SIZE, fps=FPS,
               background=(1.0, 1.0, 1.0), renderer=OpenGLRenderer())
