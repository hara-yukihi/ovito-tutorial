# Using the OVITO GUI

Using only the mouse, we will open `data/sample.xyz`, move around, analyze it, and save images.
I show you only simple examples here. Further information is available at offitial ovito manual or you can just ask ai agents.

## 1. Installation

1. Download **OVITO Basic** (free) from the Download page at https://www.ovito.org/
2. Run the installer for your OS (Windows / macOS / Linux)

> You do not need the paid OVITO Pro. Everything in this tutorial works with OVITO Basic.

## 2. Load the data

1. Click the green **Code** button of this repository → **Download ZIP**, then unzip it
2. Start OVITO and choose `data/sample.xyz` from **File → Load File**
3. If a column-mapping dialog appears, check that column 1 = `Particle Type` and columns 2–4 = `Position.X / Y / Z`, then click **OK**
4. Make sure to check `File contains multiple timesteps`. You can find this by click **Pipelines** tab at the top of the right setting box → click sample.xyz under **Data source** → See **Options** under **XYZ render** setting.
5. If you think particles are too large (they are always too large to me), you can adjust default particle size. Click **Pipelines** tab at the top of the right setting box → Click **Particles** under **Visual elements** → Change **Radius scaling** value in the **Particles display** window. It is set as 100% initially, but I prefer to set it as ~50%. You can further set particle radii with modifications.

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

## 5. Analyze / visualize with modifiers

From **Add modification...** in the pipeline panel on the right, try adding:

1. **Create bonds** - you can create bonds. There are 4 options in **Bond creation mode** pulldown. 
2. **Select type** + **Compute property** (with Compute only for selected particles option) + **Clear selection** - you can adjust color, radii, shape.. type by type. Make sure add **clear selection** when you use **Select type**: it might cause problem when you add multiple modifiers. They are like ( and ).
3. **Compute property** + **Color coding** — You can compute new value and add a column to your data by using **Compute property**. Then **Color coding** helps you to visualize.

The above list overviews properties I frequently use. You can explore more if you like.

## 6. Save movies

1. Open the **Render** tab (camera icon) at the top-right
2. Check **Save to file** and choose an output file (use a file name ending in `.mp4` or `.gif`)
3. Set Rendering range to **Complete animation** for full trajectory. If you only need specific range, set it to **Range**.
4. (optional) Click **Animation settings...** to adjust video speed.
5. (optional) Go to layer tab (next to render tab) to add layer. You can add text, coordinate tripod, or color bar in the video. Unless you subscribe ovito pro, pip ver has more options than gui ver.
6. To preview how it is shown in output, click top left corner of view point and check **preview mode**.
7. Click **Render active view point** (with camera icon. you will find this at the bottom of **Render settings**) to render.
8. (optional) You can record your best camera angle. Click top left corner of view point → Click adjust view... . Snapshot or take a note of set value so that you can reproduce it next time. However, it is hassile to manually do this on gui every time, so I recommend using pip version if you always need to keep camera angle.
