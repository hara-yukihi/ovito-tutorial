# Using OVITO from Python (pip version)

This example shows how to make an MP4 movie from an XYZ trajectory with the
`ovito` Python package (the pip version of OVITO). No GUI is needed.

The script is `render_xyz.py`.

Why use pip version? The biggest reason is that you can ask ai agent (like claude or codex) to render video or snapshot directly.

You can prompt like this: "Can you render these structure files into mp4 video using pip ver ovito?"

To describe what video you need more precisely, you can add direction (simply copy&pasting **What the script does** & **Input file format** sections below is one example. I got render_xyz.py by this.). 

However, I recommend you to examine the code line by line and execute python code manually at once to use it more effectively.

Once you know how to use pip ver ovito, you can reproduce the same operation that you can do on GUI ver ovito basic (e.g. adding modifiers, adjust rendering settings, adding text layer, ...) or even more (some operations on ovito pro (needs subscription) is not included in ovito basic on gui, but they are available on pip ver for free).

---

## What the script does

1. Reads a multi-frame XYZ file.
2. Sets the camera angle by hand (position, direction, field of view).
3. Makes all particles 50% smaller.
4. Draws bonds with **Create bonds**.
5. Changes the radius of one element only, using
   **Select type** → **Compute property** (only selected particles) → **Clear selection**.
6. Colors particles by how far they moved from frame 0, using
   **Calculate displacements** → **Compute property** → **Color coding**.
7. Shows the simulation time in fs in the upper-left corner.
8. Saves the movie as an MP4 file.

---

## Input file format

The script expects a plain XYZ file like this:

```
3
frame 0
C   0.000  0.000  0.000
H   1.090  0.000  0.000
O  -1.200  0.000  0.000
3
frame 100
C   0.010  0.000  0.000
...
```

- Line 1: number of atoms
- Line 2: `frame N` (N is the MD step number)
- Line 3 and later: element name and x y z coordinates
- This block repeats for every frame.

The time shown in the movie is computed as:

```
time [fs] = N × DT_FS
```

---

## Setup with uv

[uv](https://docs.astral.sh/uv/) is a fast Python package manager.

### 1. Install uv

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create a virtual environment

Run this in the folder that contains `render_xyz.py`:

```bash
uv venv
```

This creates a `.venv` folder.

### 3. Activate the environment

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\activate
```

### 4. Install OVITO

```bash
uv pip install ovito
```

Check that it works:

```bash
python -c "import ovito; print(ovito.version)"
```

---

## Run the script

1. Go to pip folder.
2. Edit the settings at the top of `render_xyz.py` if needed.
3. Run:

```bash
python render_xyz.py
```

The movie is saved as `sample.mp4`.

---

## Settings

All settings are at the top of `render_xyz.py`.

| Name | Meaning |
|---|---|
| `XYZ_FILE` | Input XYZ file |
| `OUT_MP4` | Output movie file |
| `DT_FS` | MD timestep in fs. Time = N × `DT_FS` |
| `TARGET_TYPE` | Element whose radius you want to change (e.g. `"O"`) |
| `TARGET_RADIUS` | New radius for that element (Å) |
| `BOND_CUTOFF` | Max distance for a bond (Å) |
| `DISP_MAX` | Upper limit of the color scale (Å) |
| `CAMERA_POS` | Camera position (x, y, z) |
| `CAMERA_DIR` | Direction the camera looks at (x, y, z) |
| `FOV_DEG` | Field of view in degrees |
| `IMAGE_SIZE` | Movie size in pixels (width, height) |
| `FPS` | Frames per second of the movie |

### Tip: finding a good camera angle

Open the same file in the OVITO GUI, rotate the view until it looks good,
then open **Adjust View...** (viewport menu). Copy the camera position,
direction, and field of view into the script.

---

## How the pipeline works

OVITO applies modifiers in order, like a list of steps. The script adds them
in this order:

```
XYZ file
  → Create bonds
  → Select type (TARGET_TYPE)
  → Compute property: Radius = TARGET_RADIUS (selected particles only)
  → Clear selection
  → Calculate displacements (reference = frame 0)
  → Compute property: Disp = |Displacement|
  → Color coding (by Disp)
  → Python function: Time = N × DT_FS
```

Notes:

- **Clear selection** is needed. If you skip it, the selected particles are
  drawn in red in the movie.
- **Compute property** cannot look at frame 0 by itself, so
  **Calculate displacements** is used first to get the displacement vectors.
- The 50% particle size is a global scale factor. It also applies to the
  radius you set with Compute property.

---

## Troubleshooting

**The movie is not created on a server without a display (HPC, SSH).**
The OpenGL renderer needs a graphics context. Change the renderer to Tachyon
(slower, but works everywhere):

```python
from ovito.vis import TachyonRenderer
...
vp.render_anim(..., renderer=TachyonRenderer())
```

**Colors look wrong when atoms cross the box boundary.**
A plain XYZ file has no cell information, so OVITO does not know about
periodic boundaries. Displacements are not unwrapped in this case.

---

## References

- OVITO Python documentation: https://docs.ovito.org/python/
- uv documentation: https://docs.astral.sh/uv/
