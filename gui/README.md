**English** | [日本語](README.ja.md)

# Using the OVITO GUI

Using only the mouse, we will open `data/sample.xyz`, move around, analyze it, and save images.

## 1. Installation

1. Download **OVITO Basic** (free) from the Download page at https://www.ovito.org/
2. Run the installer for your OS (Windows / macOS / Linux)

> You do not need the paid OVITO Pro. Everything in this tutorial works with OVITO Basic.

## 2. Load the data

1. Click the green **Code** button of this repository → **Download ZIP**, then unzip it
2. Start OVITO and choose `data/sample.xyz` from **File → Load File**
3. If a column-mapping dialog appears, check that column 1 = `Particle Type` and columns 2–4 = `Position.X / Y / Z`, then click **OK**

![After loading the file](images/01_load_file.png)

## 3. Moving the view

| Action | How |
|---|---|
| Rotate | Left-drag (Perspective view) |
| Pan | Middle-drag (or right-drag) |
| Zoom | Mouse wheel |
| Show everything | Click the viewport name at the top-left → **Adjust View / Zoom all**, or double-click |

## 4. Animation (multiple frames)

Use the time slider at the bottom to switch frames, and the ▶ button to play.
`sample.xyz` has 30 frames, and you can watch the crystal gradually become disordered.

![Time slider](images/02_timeline.png)

## 5. Analyze with modifiers

From **Add modification...** in the pipeline panel on the right, try adding:

1. **Common neighbor analysis** — colors atoms by crystal structure (green = FCC, white = Other)
2. **Slice** — set Normal to `(0, 0, 1)` and Slab width to about `4` to see a cross-section of the interior
3. **Calculate displacements** — how far each atom moved from frame 0
4. **Color coding** — set Input property to `Displacement Magnitude` to color atoms by how much they moved

![After adding modifiers](images/03_modifiers.png)

> Surface atoms are white (not FCC) because the system has no periodic boundaries, so they lack enough neighbors. Look inside with Slice and you will see green atoms.

## 6. Save images and movies

1. Open the **Render** tab (camera icon) at the top-right
2. Check **Save to file** and choose an output file
3. Still image: **Render active viewport**
4. Movie: set Rendering range to **Complete animation**, use a file name ending in `.mp4` or `.gif`, then render

![Render settings](images/04_render.png)

## 7. Save your session

**File → Save Session State** saves your modifiers and view as an `.ovito` file, so you can open it later and continue from the same state.
